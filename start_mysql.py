import mysql.connector as mysql
import subprocess
import time

print("Starting MySQL...")
subprocess.run(["sudo", "systemctl", "start", "mysql"])
time.sleep(3)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test"
    )
    print("Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print(f"MySQL connection failed: {err}")
