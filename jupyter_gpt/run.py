import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

run_path = "workspace/"
notebook_filename = "workspace/notebook.ipynb"
notebook_filename_out = "workspace/notebook.ipynb"

def run():
    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600_000, kernel_name='python3')

    try:
        out = ep.preprocess(nb, {'metadata': {'path': run_path}})
    except CellExecutionError:
        out = None
        msg = 'Error executing the notebook "%s".\n\n' % notebook_filename
        msg += 'See notebook "%s" for the traceback.' % notebook_filename_out

        return False

    finally:
        with open(notebook_filename_out, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)
    
    return True