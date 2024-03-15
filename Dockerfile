FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app


COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 9090