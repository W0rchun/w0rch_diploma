#!/bin/bash

# Ожидание RabbitMQ
/wait-for-it.sh rabbitmq:5672 --timeout=30 --strict -- echo "RabbitMQ is up"

# Запуск main.py
python connection.py -- echo "connection is up" &

# Ожидание, пока main.py инициализируется
sleep 5

# Запуск connection.py
python main.py
