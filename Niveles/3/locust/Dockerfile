FROM locustio/locust
COPY ./requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
COPY ./locustfile.py locustfile.py
