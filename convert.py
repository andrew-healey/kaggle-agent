with open("/opt/conda/lib/python3.10/site-packages/nbclient/client.py","r") as f:
    nbclient_source = f.read()

"""
After this line:
    def process_message(
        self, msg: t.Dict, cell: NotebookNode, cell_index: int
    ) -> t.Optional[t.List]:
Add this line:
        try:
            print("Client saving")
            self.save()
        except:
            print("Client save failed")
"""

old_str = """
    def process_message(
        self, msg: t.Dict, cell: NotebookNode, cell_index: int
    ) -> t.Optional[t.List]:
"""
new_str = old_str+"\n"+"""
        try:
            print("Client saving")
            self.save()
        except:
            print("Client save failed")
"""

new_source = nbclient_source.replace(old_str,new_str)

# with open("/opt/conda/lib/python3.10/site-packages/nbclient/client.py","w") as f:
#     f.write(new_source)

print("Done!")