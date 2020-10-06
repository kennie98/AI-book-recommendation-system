FROM python:3.7-alpine

WORKDIR /service

ADD . /service

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]