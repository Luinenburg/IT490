import pika
import sys
import mysql.connector as mysql
import time

def connect_rabbitmq(rabbitmq_ip):
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip))
    channel = connection.channel()
    channel.queue_declare(queue='test')
    channel.basic_publish(exchange='', routing_key='test', body='Testing Connection...')
    channel.close()
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip))
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get('test')
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        if body != b'Testing Connection...':
            print(f"Wrong message in queue: {body}")
    else:
        print("No message in queue.")
        connection.close()
        return
    print(f"Connection made on {rabbitmq_ip}")
    return (connection, channel)

def connect_mysql(mysql_ip):
    try:
        mysql_connection = mysql.connect(host = mysql_ip, user='test', passwd='test', database='test')
    except mysql.Error as err:
        print("Unable to connect to MySQL")
        print(err)
        return
    print(f"Connection Made to MySQL on {mysql_ip}")
    return mysql_connection

def main():
    connect_rabbitmq('localhost')
    connect_mysql('localhost')

if __name__=="__main__":
    main()