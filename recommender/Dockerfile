FROM python:3.7

WORKDIR /service

ADD . /service

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y curl

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
