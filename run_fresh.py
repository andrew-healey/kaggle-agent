import nbformat
from nbclient import NotebookClient

nb = nbformat.read("workspace/notebook.ipynb", as_version=4)
client = NotebookClient(nb, timeout=60_000, kernel_name='python3', resources={'metadata': {'path': 'workspace/'}})

client.save = lambda *args: nbformat.write(nb, 'executed_notebook.ipynb')

client.execute()
nbformat.write(nb, 'executed_notebook.ipynb')

print("Done")