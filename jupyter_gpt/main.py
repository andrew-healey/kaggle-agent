from .functions import complete_with_functions
from .tools import functions
from .stringifyIpynb import stringifyIpynb

print("Enter your request")
user_request = input()

while True:
    system_prompt = f"""
    You are JupyterGPT. You have been asked to complete a task in a Jupyter notebook.
    The task is: {user_request}
    First, lay out the steps you will take to complete the task. Think step by step.
    Then write the code to complete the task.
    Note: you should run your code infrequently, as this computer is very slow.
    Never use tensorflow or keras - prefer pytorch.

    Notebook contents:
    {stringifyIpynb("workspace/notebook.ipynb")[0]}
    """

    try:
        response = complete_with_functions(system_prompt, *functions)
    except Exception as e:
        if "maximum context length" in str(e):
            print("Context overflowed, continuing with fresh context")
        else:
            raise e
    
    break

print(response)