FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

WORKDIR /connection

RUN pip install pika requests

#копирование кода
COPY . /connection

# COPY wait-for-it.sh /wait-for-it.sh
# RUN chmod +x /wait-for-it.sh


CMD ["python3", "connection.py"]
