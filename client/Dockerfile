FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY start-client.sh client.py requirements.txt ./

RUN apk add --no-cache curl

RUN pip install -r requirements.txt

CMD ["./start-client.sh"]
