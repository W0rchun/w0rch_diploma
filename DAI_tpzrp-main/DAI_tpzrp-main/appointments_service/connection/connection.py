import pika
import json
import os, sys
import requests
import time
import logging


RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))



def main():
    time.sleep(40)
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='set_free_appointment')


    def appointment_callback(ch, method, properties, body):
        _body = json.loads(body)

        print("_body before pop", _body)
        appointment_id = _body['id_in_appointment_service']
        _body.pop('id_in_appointment_service')

        access_token = _body['access_token']
        _body.pop('access_token')

        print(f" [x] Received from appointments queue {_body}")
        
        response = requests.put(f"http://appointments_service:5003/{appointment_id}", data = json.dumps(_body), cookies={'token': access_token})
        print(response.text)


    channel.basic_consume(queue='set_free_appointment', on_message_callback=appointment_callback, auto_ack=True)
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