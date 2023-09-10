import json

import tiktoken
# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")

max_src_len = 2000
max_output_len = 500
max_line_len = 200

def compress(string:str,max_tokens:int=max_output_len)->str:
    tokens = enc.encode(string)
    if len(tokens) > max_tokens + 20:
        return enc.decode(tokens[:max_tokens//2]) + "... <truncated for length> ..." + enc.decode(tokens[-max_tokens//2:])
    return string

from typing import List
def stringify_lines(lines:List[str],max_tokens:int=max_output_len,max_line_tokens:int=max_line_len)->str:
    return compress("".join(compress(line,max_line_tokens) for line in lines),max_tokens)+"\n"

def fences(string:str,lang:str="")->str:
    return f"```{lang}\n{string}\n```\n"

def stringifyIpynb(path):

    failed_cell_num = -1

    out = ""
    with open(path) as f:
        nb = json.load(f)

        if len(nb["cells"]) == 0:
            return "<notebook is empty>",-1

        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                out += f"In [{cell['execution_count']}]:\n"
                src = stringify_lines(cell["source"],max_src_len)
                out += fences(src,"python")

                # outputs
                for output in cell["outputs"]:
                    if output["output_type"] == "error":
                        err = "\n".join(output["traceback"])+"\n"
                        out += fences(err)
                        failed_cell_num = cell["execution_count"]
                    elif output["output_type"] == "stream":
                        out += fences(stringify_lines(output["text"]))
                    elif output["output_type"] == "display_data":
                        out += fences(stringify_lines(output["data"]["text/plain"]))
            elif cell["cell_type"] == "markdown":
                out += fences(stringify_lines(cell["source"],max_src_len),"md")
            else:
                raise Exception(f"Unknown cell type {cell['cell_type']}")
        
    return out, failed_cell_num

if __name__ == "__main__":
    as_str = (stringifyIpynb("workspace/notebook.ipynb"))
    with open("workspace/notebook_out.md","w") as f:
        f.write(as_str[0])