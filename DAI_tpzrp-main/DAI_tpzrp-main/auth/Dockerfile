FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

#рабочая директория
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

#копирование кода
COPY . /app
# Добавьте скрипт ожидания в контейнер
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x wait-for-it.sh

#микросервис на 5002 порту
EXPOSE 5002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002", "--reload"]
