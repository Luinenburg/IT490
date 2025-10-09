#!/bin/env python
import pika, sys, os, mysql.connector as mysql


sys.path.append('path/to/django/folder')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def send_message(message):
    connection = pika.BlockingConnection(rabbitmq)
    channel = connection.channel()

    # Declare queue (durable)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Publish persistent message
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        )
    )
    print(f"Sent: {message}")
    connection.close()



def connect_rabbitmq(rabbitmq_ip):
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip))
    channel = connection.channel()

    channel.queue_declare(queue='hello',durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def main():
    connect_rabbitmq('localhost')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Send or receive messages from RabbitMQ")
    parser.add_argument('--send', type=str, help='Send a message to the queue')
    parser.add_argument('--consume', action='store_true', help='Start consuming messages')
    args = parser.parse_args()

    if args.send:
        send_message(args.send)
    elif args.consume:
        consume('localhost')
    else:
        print("Use --send <message> to send or --consume to receive messages")
