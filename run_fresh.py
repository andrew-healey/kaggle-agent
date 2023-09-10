# read filename from command line
import sys
filename = sys.argv[1]
assert filename.endswith('.ipynb'), "File must be a Jupyter notebook"

import nbformat
from nbclient import NotebookClient

nb = nbformat.read(filename, as_version=4)
client = NotebookClient(nb, timeout=60_000, kernel_name='python3', resources={'metadata': {'path': 'workspace/'}})

def save(*args):
    nbformat.write(nb, filename)

client.save = save

client.execute()
save()

print("Done")