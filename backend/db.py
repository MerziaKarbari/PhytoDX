import os
import mysql.connector
from mysql.connector import Error
import bcrypt


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Connect to Aiven MySQL database"""
        try:
            if self.connection is None or not self.connection.is_connected():
                base_dir = os.path.dirname(os.path.abspath(__file__))
                ssl_ca = os.path.join(base_dir, "ca.pem")

                self.connection = mysql.connector.connect(
                    host=os.environ.get("MYSQL_HOST"),
                    port=int(os.environ.get("MYSQL_PORT", 3306)),
                    user=os.environ.get("MYSQL_USER"),
                    password=os.environ.get("MYSQL_PASSWORD"),
                    database=os.environ.get("MYSQL_DATABASE"),
                    ssl_ca=ssl_ca,
                    connection_timeout=10
                )
                print("Database connected successfully!")

            return self.connection

        except Error as e:
            print(f"Database connection error: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Execute INSERT, UPDATE or DELETE query"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def register_user(self, name, email, password, phone=""):
        """Register a new user"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT user_id FROM USERS WHERE email = %s",
                (email,)
            )

            if cursor.fetchone():
                return {
                    "success": False,
                    "message": "Email already registered"
                }

            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            cursor.execute(
                """
                INSERT INTO USERS (name, email, password, phone)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, hashed_password, phone)
            )

            self.connection.commit()

            return {
                "success": True,
                "message": "Registration successful",
                "user_id": cursor.lastrowid
            }

        except Error as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": str(e)
            }
        finally:
            cursor.close()

    def login_user(self, email, password):
        """Login an existing user"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM USERS WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()

            if not user:
                return {
                    "success": False,
                    "message": "Invalid email or password"
                }

            stored_password = user.get("password", "")

            if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            ):
                return {
                    "success": True,
                    "message": "Login successful",
                    "user": {
                        "user_id": user["user_id"],
                        "name": user["name"],
                        "email": user["email"]
                    }
                }

            return {
                "success": False,
                "message": "Invalid email or password"
            }

        finally:
            cursor.close()

    def get_all_diseases(self):
        """Get all diseases"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM DISEASES")
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_disease_by_name(self, disease_name):
        """Get a disease by its name"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM DISEASES WHERE disease_name = %s",
                (disease_name,)
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def get_disease_with_treatment(self, disease_name):
        """Get disease details and treatment"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = """
                SELECT d.*, t.*
                FROM DISEASES d
                LEFT JOIN TREATMENTS t
                    ON d.disease_id = t.disease_id
                WHERE d.disease_name = %s
            """
            cursor.execute(query, (disease_name,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def save_scan(self, user_id, disease_id, image_path, confidence):
        """Save a scan in scan history"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO SCAN_HISTORY
                (user_id, disease_id, image_path, confidence)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, disease_id, image_path, confidence)
            )
            self.connection.commit()

            return {
                "success": True,
                "message": "Scan saved successfully",
                "scan_id": cursor.lastrowid
            }

        except Error as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": str(e)
            }
        finally:
            cursor.close()

    def get_user_scans(self, user_id):
        """Get scan history for a user"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = """
                SELECT s.*, d.disease_name
                FROM SCAN_HISTORY s
                LEFT JOIN DISEASES d
                    ON s.disease_id = d.disease_id
                WHERE s.user_id = %s
                ORDER BY s.scan_id DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
