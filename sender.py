import json

import pika


def pika_task(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='send_mail')

    channel.basic_publish(exchange='', routing_key='send_mail', body=json.dumps(body))
    print(f" [x] Sent {json.dumps(body)}")
    connection.close()


