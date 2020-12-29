FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt
