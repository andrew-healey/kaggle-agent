docker build -t kaggle-mine .
cp notebook_template.ipynb workspace/notebook.ipynb
docker run --rm -it -v $(pwd)/input:/input -v $(pwd)/workspace:/workspace -e OPENAI_API_KEY=$OPENAI_API_KEY kaggle-mine