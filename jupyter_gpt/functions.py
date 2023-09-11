import json
from inspect import signature
import os

from docstring_parser import parse
import openai
from .print import print_system_text,print_agent_response

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4"


def complete_with_functions(question, *functions):
    """
    Call the openai completion function with specified functions
    to be called optionally. The function signatures can be parsed
    automatically.

    :param question:
    :param functions:
    :return:
    """
    # TODO extend to parsing openapi docs
    req = {
        "model": MODEL,
        "messages": [{"role": "system", "content": question}] if type(question) == str else question,
        "functions": [parse_function(f) for f in functions],
        "stream": True
    }
    with open("workspace/req.json", "w") as f:
        json.dump(req, f, indent=2)
    
    response = openai.ChatCompletion.create(**req)
    partial_message = {
        "role":None,
        "content":None,
        "function_call":None
    }
    finish_reason = None
    deltas = []
    for chunk in response:
        choice = chunk["choices"][0]
        delta = choice["delta"]
        deltas.append(delta)
        # print(choice)
        if choice["finish_reason"] is not None:
            finish_reason = choice["finish_reason"]
            assert delta == {},"Ending delta should be empty"
            break
        else:
            if "role" in delta:
                partial_message["role"] = delta["role"]
            elif delta.get("content") is not None:
                # print new content on same line
                print_agent_response(delta["content"],end="")

                partial_message["content"] = (partial_message["content"] or "") + delta["content"]
            if "function_call" in delta:
                function_call = delta["function_call"]
                if partial_message["function_call"] is None:
                    partial_message["function_call"] = function_call
                else:
                    assert "arguments" in function_call,"Function call should have arguments if it's a streaming response"
                    partial_message["function_call"]["arguments"] += function_call["arguments"]
    
    if partial_message["content"] is not None:
        print()
            
    if finish_reason != "function_call":
        return partial_message["content"]
    
    with open("workspace/deltas.json", "w") as f:
        json.dump(deltas, f, indent=2)
    assert partial_message["role"] is not None,"Role should be defined"
    assert partial_message["function_call"] is not None,"Function call should be defined"

    messages,should_continue = call_functions(partial_message, *functions)
    req["messages"].extend(messages)

    with open("workspace/req.json", "w") as f:
        json.dump(req, f, indent=2)

    if should_continue:
        return complete_with_functions(req["messages"], *functions)
    else:
        return "Stopped by function call"


def call_functions(msg, *functions):
    """Execute the functions using the initial responses.

    :param response:
    :param functions:
    :return:
    """
    messages = []
    should_continue = False

    messages.append(msg)
    func_data = msg["function_call"]
    try:
        args = json.loads(func_data["arguments"])
    except:
        raise Exception("Error parsing arguments for function call")
        print("Error parsing arguments for function call")
        print("Function call:", func_data)
        input("What to do?")
    name = func_data["name"]
    for f in functions:
        if f.__name__ == name:
            try:
                result = f(**args)
            except Exception as e:
                result = f"Error: {e}"
            if result != "__pass__":
                should_continue = True
            messages.append(
                {
                    "role": "function",
                    "name": name,
                    "content": json.dumps(result),
                }
            )
    return messages, should_continue


def parse_annotation(annotation):
    """Convert the type annotation to type string for json

    :param annotation:
    :return:
    """
    # TODO how to reliably map python type hint to json type?
    return {"str": "string", "int": "number", "float": "number", "bool": "boolean"}[
        annotation.__name__
    ]


def parse_parameter(annotation, docs):
    """Convert the parameter signature and docstring
    to json for function API.

    :param annotation:
    :param docs:
    :return:
    """
    type_name = parse_annotation(annotation)
    return {
        "type": type_name,
        "description": docs.description if docs is not None else "",
    }


def parse_function(func):
    """
    Parse the docstring and type annotations
    to automatically create a signature for GPT functions

    :param func:
    :return:
    """
    docs = parse(func.__doc__)
    param_docs = {p.arg_name: p for p in docs.params}
    sig = signature(func)
    required = [
        k for k, v in sig.parameters.items() if v.kind == v.POSITIONAL_OR_KEYWORD
    ]

    properties = {
        name: parse_parameter(p.annotation, param_docs.get(name))
        for name, p in sig.parameters.items()
    }
    descriptor = {
        "name": func.__name__,
        "description": docs.short_description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }
    return descriptor