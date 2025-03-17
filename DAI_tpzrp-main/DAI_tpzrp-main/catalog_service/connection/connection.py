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
    channel.queue_declare(queue='regions')
    channel.queue_declare(queue='med_orgs')
    channel.queue_declare(queue='subdivisions')
    channel.queue_declare(queue='doctors')

    def regions_callback(ch, method, properties, body):
        _body = json.loads(body)
        print(f" [x] Received from regions queue {_body}")
    
        response = requests.post(f"http://catalog_service:5004/regions/", data = json.dumps(_body))

        print(response.text)

    def med_orgs_callback(ch, method, properties, body):
        _body = json.loads(body)
        print(f" [x] Received from med_orgs queue {_body}")
        
        response = requests.post(f"http://catalog_service:5004/organizations/", data = json.dumps(_body))

        print(response.text)

    def subdivisions_callback(ch, method, properties, body):
        _body = json.loads(body)
        print(f" [x] Received from subdivisions queue {_body}")
        
        response = requests.post(f"http://catalog_service:5004/subdivisions/", data = json.dumps(_body))

        print(response.text)

    def doctors_callback(ch, method, properties, body):
        _body = json.loads(body)
        print(f" [x] Received from doctors queue {_body}")
        
        response = requests.post(f"http://catalog_service:5004/doctors/", data = json.dumps(_body))

        print(response.text)

    channel.basic_consume(queue='regions', on_message_callback=regions_callback, auto_ack=True)
    channel.basic_consume(queue='med_orgs', on_message_callback=med_orgs_callback, auto_ack=True)
    channel.basic_consume(queue='subdivisions', on_message_callback=subdivisions_callback, auto_ack=True)
    channel.basic_consume(queue='doctors', on_message_callback=doctors_callback, auto_ack=True)
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
