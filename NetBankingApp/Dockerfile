FROM python:3.8-alpine

WORKDIR /home/NetBankingApp/.
COPY requirements.txt /home/NetBankingApp/requirements.txt

RUN apk update && apk add gcc python3-dev zlib-dev jpeg-dev musl-dev
RUN pip install --no-cache-dir -r /home/NetBankingApp/requirements.txt

EXPOSE 8000
