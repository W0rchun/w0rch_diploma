import requests
import os, sys
import pika
import json
import time

RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

def main():
    time.sleep(30)
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='appointments')

    def appointment_callback(ch, method, properties, body):
        _body = json.loads(body)
        print(f" [x] Received from appointments queue {_body}")
        
        response = requests.post("http://patient_service:5005/appointments/", data = json.dumps(_body))

        print(response.text)


    channel.basic_consume(queue='appointments', on_message_callback=appointment_callback, auto_ack=True)
    print('Consuming started')
    channel.start_consuming()


if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
