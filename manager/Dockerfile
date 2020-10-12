FROM python:3.7-alpine

WORKDIR /service

ADD . /service

RUN pip install -r requirements.txt

RUN apk add --update curl && rm -rf /var/cache/apk/*

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
