import os
import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():

                host = os.environ.get("MYSQL_HOST")
                port = int(os.environ.get("MYSQL_PORT", 3306))
                user = os.environ.get("MYSQL_USER")
                password = os.environ.get("MYSQL_PASSWORD")
                database = os.environ.get("MYSQL_DATABASE")

                # backend folder mein ca.pem file ka path
                base_dir = os.path.dirname(os.path.abspath(__file__))
                ssl_ca = os.path.join(base_dir, "ca.pem")

                self.connection = mysql.connector.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database,
                    ssl_ca=ssl_ca,
                    connection_timeout=10
                )

                print("Database connected successfully!")

            return self.connection

        except Error as e:
            print(f"Database connection error: {e}")
            raise
