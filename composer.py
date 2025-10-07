import pika 
import mysql.connector as mysql
import json 
import sys
import time

def connect_db(): 
    return mysql.connector.connect( 
        host="localhost", 
        user="test", 
        password="test", 
        database="test" 
    ) 

def fetch_users(limit=5):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM users LIMIT %s;", (limit,))
    rows = cursor.fetchall()
    db.close()
    return rows

def publish_messages(channel, rows):
    for row in rows:
        message = json.dumps(row)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f" [x] Sent {message}")

def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    print(f" [x] Received {data}")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO logs (message) VALUES (%s)", (str(data),))
    db.commit()
    db.close()
    ch.basic_ack(delivery_tag=method.delivery_tag) 
    
def main():
    try:
        print("Connecting to RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        
        print("Fetching users from DB...")
        rows = fetch_users(limit=5)
        publish_messages(channel, rows)
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            channel.stop_consuming()
        except Exception:
            pass
        connection.close()
        sys.exit(0)
        
if __name__ == "__main__":
    time.sleep(5) 
    main()