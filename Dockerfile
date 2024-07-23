FROM python:3.12.4

WORKDIR /QRNG_API

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

