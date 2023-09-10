# run a python process -c "import nbclient; print(nbclient.__file__)"
import subprocess
import os

# get the path to nbclient
nbclient_path = subprocess.check_output(["python","-c","import nbclient; print(nbclient.__file__)"]).decode("utf-8").strip()
# switch the __init__.py to client.py
client_path = os.path.join(os.path.dirname(nbclient_path),"client.py")

with open(client_path,"r") as f:
    nbclient_source = f.read()

old_str = """
    def process_message(
        self, msg: t.Dict, cell: NotebookNode, cell_index: int
    ) -> t.Optional[NotebookNode]:
"""
new_str = old_str+"\n"+"""
        try:
            self.save()
        except:
            print("Client save failed")
"""

if new_str in nbclient_source:
    print("Already patched")
    exit()

new_source = nbclient_source.replace(old_str,new_str)

with open(client_path,"w") as f:
    f.write(new_source)

print("Done!")