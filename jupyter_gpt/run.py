import nbformat
from nbclient import NotebookClient
import nbclient

run_path = "workspace/"
notebook_filename = "workspace/notebook.ipynb"
notebook_filename_out = "workspace/notebook_out.ipynb"

def run():

    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)
        client = NotebookClient(nb, timeout=600_000, kernel_name='python3', resources={'metadata': {'path': 'notebooks/'}})
        def save():
            print("Saving")
            with open(notebook_filename_out, mode='w', encoding='utf-8') as f:
                nbformat.write(nb, f)
        client.save = save

    try:
        client.execute()
    except:
        msg = 'Error executing the notebook "%s".\n\n' % notebook_filename
        msg += 'See notebook "%s" for the traceback.' % notebook_filename_out

        return False

    finally:
        save()
    
    return True


def run():

    nb = nbformat.read("workspace/notebook.ipynb", as_version=4)
    client = NotebookClient(nb, timeout=60_000, kernel_name='python3', resources={'metadata': {'path': 'workspace/'}})

    client.save = lambda *args: nbformat.write(nb, 'workspace/notebook.ipynb')

    client.execute()
    nbformat.write(nb, 'workspace/notebook.ipynb')

    # print("Done")