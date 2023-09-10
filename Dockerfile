# docker run --rm -it gcr.io/kaggle-images/python /bin/bash
FROM gcr.io/kaggle-images/python
#us-docker.pkg.dev/colab-images/public/runtime
#

RUN pip install nbconvert
RUN pip install openai docstring_parser tiktoken

COPY jupyter_gpt /jupyter_gpt

# run jupyter nbconvert --execute --to notebook workspace/output.ipynb
CMD ["python", "-m", "jupyter_gpt.main"]

# give container access to ./workspace in host
# docker run --rm -it -v $(pwd)/workspace:/workspace kaggle-mine /bin/bash