# syntax = docker/dockerfile:1.4

FROM python:3.11-slim AS builder

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./server /code/server

CMD ["uvicorn", "--app-dir", "server", "main:app", "--host", "0.0.0.0", "--port", "8000"]
