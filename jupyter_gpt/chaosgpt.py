from .functions import complete_with_functions
from .tools import edit_python_cell,run_notebook
from .stringifyIpynb import stringifyIpynb
from .run import run

system_prompt = f"""
You are JupyterSabotager. You have been asked to introduce bugs into a Jupyter notebook.
These bugs should preferably lead to errors later on in the notebook.

Notebook contents:
{stringifyIpynb("workspace/notebook.ipynb")[0]}
"""

response = complete_with_functions(system_prompt, edit_python_cell, run_notebook)

run()

print("Done! I've added several subtle bugs to the notebook.")