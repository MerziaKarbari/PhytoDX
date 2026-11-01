import os
import mysql.connector
from mysql.connector import Error

connection = None

def connect():
    global connection

    try:
        if connection is None or not connection.is_connected():

            host = os.environ.get("MYSQL_HOST")
            port = int(os.environ.get("MYSQL_PORT", 3306))
            user = os.environ.get("MYSQL_USER")
            password = os.environ.get("MYSQL_PASSWORD")
            database = os.environ.get("MYSQL_DATABASE")

            # SSL certificate ka absolute path
            base_dir = os.path.dirname(os.path.abspath(__file__))
            ssl_ca = os.path.join(base_dir, "ca.pem")

            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                ssl_ca=ssl_ca,
                connection_timeout=10
            )

            print("Database connected successfully!")

        return connection

    except Error as e:
        print(f"Database connection error: {e}")
        raise
