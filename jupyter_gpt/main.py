from .functions import complete_with_functions
from .tools import functions
from .stringifyIpynb import stringifyIpynb
from .print import print_agent_response, print_system_text

import os

# mkdir kaggle/
if not os.path.exists("kaggle"):
    os.mkdir("kaggle")

# download from kaggle link
print_system_text("Paste kaggle download code (leave blank to skip)")
notebook_cmd = input()
if len(notebook_cmd) > 0:
    os.system(notebook_cmd+" -p kaggle/")
    os.system("mv kaggle/* workspace/notebook.ipynb")

print_agent_response("What would you like me to do?")
user_request = input()

# get list of files in workspace
from os import listdir
from os.path import isfile, join
files = [f for f in listdir("workspace") if isfile(join("workspace", f))]
# to str
files = ",".join(files)

while True:
    system_prompt = f"""
    You are JupyterGPT. You have been asked to complete a task in a Jupyter notebook.
    The task is: {user_request}
    First, lay out the steps you will take to complete the task. Think step by step.
    Then write the code to complete the task.
    Run your code often to make sure it works.
    Never use tensorflow or keras - prefer pytorch.

    Workspace contents: {files}

    Notebook contents:
    {stringifyIpynb("workspace/notebook.ipynb")[0]}
    """

    try:
        response = complete_with_functions(system_prompt, *functions)
        break
    except Exception as e:
        if "maximum context length" in str(e):
            print("Context overflowed, continuing with fresh context")
        elif "Error parsing arguments":
            print("Error parsing arguments, continuing with fresh context")
        else:
            raise e
    

print("Done!")