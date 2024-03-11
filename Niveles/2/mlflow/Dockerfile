FROM python:3.9
ARG MLFLOW_S3_ENDPOINT_URL=http://10.43.102.109:9000
ARG AWS_ACCESS_KEY_ID=admin
ARG AWS_SECRET_ACCESS_KEY=supersecret
RUN mkdir /work
WORKDIR /work
COPY . .
RUN pip install jupyter==1.0.0 -U && pip install jupyterlab==3.6.1
RUN pip install -r requirements.txt
EXPOSE 8888
ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]