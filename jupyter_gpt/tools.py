from .stringifyIpynb import stringifyIpynb

import json

def str_to_source(string:str):
    return [line+"\n" for line in string.split("\n")]

def append_new_cell(lang:str, cell_source:str):
    """
    Appends a new cell to the end of the notebook.
    Language can be "python" or "markdown"
    """

    print(f"Appending new {lang} cell")
    # print(f"Source: {cell_source}")

    assert lang in ["python", "markdown"], "Language must be python or markdown"

    with open("workspace/notebook.ipynb") as f:
        nb = json.load(f)

    if lang == "markdown":
        new_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": str_to_source(cell_source),
        }
    elif lang == "python":
        new_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": str_to_source(cell_source),
        }
    
    nb["cells"].append(new_cell)
    with open("workspace/notebook.ipynb","w") as f:
        json.dump(nb,f)
    
    return "Successfully appended cell!"

def edit_python_cell(cell_num:int,new_source:str):
    """
    Edits the source of a Python cell in the notebook.
    The cell_num should be pulled from i.e. "In [1]:"
    cell_num is 1-indexed.
    """

    print(f"Editing cell {cell_num}")

    with open("workspace/notebook.ipynb") as f:
        nb = json.load(f)

    wrote_cell = False
    cell_nums = [cell.get("execution_count",-1) for cell in nb["cells"]]
    for cell in nb["cells"]:
        if cell["cell_type"] == "code" and cell["execution_count"] == cell_num:

            cell["source"] = str_to_source(new_source)
            wrote_cell = True
            break
    
    if not wrote_cell:
        print(f"Could not find cell {json.dumps(cell_num)} - cell nums are {json.dumps(cell_nums)}")
        raise Exception(f"Cell {cell_num} does not exist! Remember to use the number from i.e. 'In [1]:'")

    with open("workspace/notebook.ipynb","w") as f:
        json.dump(nb,f)
    
    return "Successfully edited cell!"

from .run import run
def run_notebook():
    """
    Runs the notebook!
    Use this function to check your work and look for bugs.
    Use this function liberally.
    """

    print("Running notebook...")
    try:
        run()
    except Exception as e:
        print("Error running notebook!")
        print(e)
        raise e
    print("Ran notebook")

    new_ipynb,failed_cell_num = stringifyIpynb("workspace/notebook.ipynb")
    did_fail = failed_cell_num != -1

    return f"""
Ran notebook.

{new_ipynb}

Run status: {"An error was thrown at cell "+str(failed_cell_num) if did_fail else "No errors detected."}"""

def exit():
    """
    Exits the Jupyter notebook - only call this when you are done!
    """

    print("Exiting...")
    return "__pass__"

functions = [
    append_new_cell,
    edit_python_cell,
    run_notebook,
    exit,
]