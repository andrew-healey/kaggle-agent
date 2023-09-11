import bs4 as bs
import urllib.request
import json

import os

def download_notebook(url):
    # get notebook html

    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source,'lxml')

    # find a tag #site-body > script.kaggle-component:nth-child(2)
    script = soup.find_all("script",class_="kaggle-component")[0]
    """
    Script looks something like this:
<some crap here>Kaggle.State.push({
    < ... valuable config data ... >
});<some crap here>
    """

    # extract the config data
    script = str(script)
    prefix = "Kaggle.State.push("
    suffix = "});"

    first_prefix_index = script.index(prefix)
    last_suffix_index = script.rindex(suffix)

    data = script[first_prefix_index+len(prefix):last_suffix_index+1]
    data = json.loads(data)

    with open("workspace/config.json","w") as f:
        json.dump(data,f,indent=2)

    # baseurl = /code/<author>/<notebook>
    baseurl = data["baseUrl"]
    _,_,author,notebook = baseurl.split("/")

    notebook_download_cmd = f"kaggle kernels pull -p kaggle/ {author}/{notebook}"

    os.system(notebook_download_cmd)
    os.system("mv kaggle/* workspace/notebook.ipynb")

    assert len(data["dataSources"]) == len(data["renderableDataSources"]),"All data sources should be renderable"

    for data_source in data["renderableDataSources"]:
        mount_slug = data_source["reference"]["mountSlug"]

        data_source_url = data_source["dataSourceUrl"]
        assert data_source_url.startswith("/datasets/"),"Data source url should start with /datasets/"
        source_url = data_source_url[10:] # remove /datasets/

        # donwload to input/<mount_slug>

        out_dir = f"input/{mount_slug}" if len(mount_slug) > 0 else "input"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        data_download_cmd = f"kaggle datasets download -p {out_dir} {source_url}"

        os.system(data_download_cmd)

        # unzip (replace existing files)
        os.system(f"unzip -o {out_dir}/*.zip -d {out_dir}")
        # remove zip
        os.system(f"rm {out_dir}/*.zip")


if __name__ == "__main__":
    download_notebook("https://www.kaggle.com/code/shahidulugvcse/visualization/notebook")