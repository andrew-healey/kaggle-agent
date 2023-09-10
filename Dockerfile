# docker run --rm -it gcr.io/kaggle-images/python /bin/bash
FROM gcr.io/kaggle-images/python
#us-docker.pkg.dev/colab-images/public/runtime
#

RUN pip install nbconvert nbclient
RUN pip install openai docstring_parser tiktoken

COPY kaggle.json /root/.kaggle/kaggle.json

COPY convert.py /convert.py
RUN python /convert.py

# RUN cp /opt/conda/lib/python3.10/site-packages/nbclient/client.py /old_client.py
# COPY old_client.py /opt/conda/lib/python3.10/site-packages/nbclient/client.py

COPY jupyter_gpt /jupyter_gpt

# run jupyter nbconvert --execute --to notebook workspace/output.ipynb
CMD ["python", "-m", "jupyter_gpt.main"]

# give container access to ./workspace in host
# docker run --rm -it -v $(pwd)/workspace:/workspace kaggle-mine /bin/bash