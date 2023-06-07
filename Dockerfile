FROM python:3.10.6-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /reservation

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .