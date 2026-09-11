# backend/db.py
# This file handles all database operations

import mysql.connector
from config import Config

class Database:
    """Handles all database operations"""
    
    def __init__(self):
        """Set up database settings"""
        self.config = Config()
        self.connection = None
    
    def connect(self):
        """Connect to MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config.MYSQL_HOST,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD,
                database=self.config.MYSQL_DATABASE
            )
            print("✅ Database connected!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database disconnected")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                cursor.close()
                return result
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"❌ Query error: {e}")
            return None
    
    # ---------- DISEASE FUNCTIONS ----------
    
    def get_all_diseases(self):
        """Get all diseases from database"""
        query = "SELECT * FROM DISEASES"
        return self.execute_query(query) or []
    
    def get_disease_by_name(self, disease_name):
        """Get disease by name"""
        query = "SELECT * FROM DISEASES WHERE disease_name = %s"
        result = self.execute_query(query, (disease_name,))
        if result and len(result) > 0:
            return result[0]
        return None
    
    def get_disease_by_id(self, disease_id):
        """Get disease by ID"""
        query = "SELECT * FROM DISEASES WHERE disease_id = %s"
        result = self.execute_query(query, (disease_id,))
        if result and len(result) > 0:
            return result[0]
        return None
    
    def get_disease_with_treatment(self, disease_name):
        """Get disease with its treatment"""
        disease = self.get_disease_by_name(disease_name)
        if not disease:
            return None
        
        # Get treatment for this disease
        query = "SELECT * FROM TREATMENTS WHERE disease_id = %s"
        treatments = self.execute_query(query, (disease['disease_id'],))
        treatment = treatments[0] if treatments and len(treatments) > 0 else None
        
        return {
            "disease": disease,
            "treatment": treatment
        }
    
    # ---------- USER FUNCTIONS ----------
    
    def get_user_by_email(self, email):
        """Get user by email"""
        query = "SELECT * FROM USERS WHERE email = %s"
        result = self.execute_query(query, (email,))
        if result and len(result) > 0:
            return result[0]
        return None
    
    def register_user(self, name, email, password, phone=None):
        """Register a new user"""
        # Check if user exists
        existing = self.get_user_by_email(email)
        if existing:
            return {"success": False, "message": "User already exists"}
        
        # Insert new user
        query = "INSERT INTO USERS (name, email, password, phone) VALUES (%s, %s, %s, %s)"
        params = (name, email, password, phone)
        
        result = self.execute_query(query, params)
        if result:
            return {"success": True, "message": "User registered successfully"}
        return {"success": False, "message": "Registration failed"}
    
    def login_user(self, email, password):
        """Login user"""
        user = self.get_user_by_email(email)
        if not user:
            return {"success": False, "message": "User not found"}
        
        # For now, compare plain text (we'll add hashing later)
        if user['password'] == password:
            user.pop('password', None)
            return {"success": True, "message": "Login successful", "user": user}
        
        return {"success": False, "message": "Invalid password"}
    
    # ---------- SCAN HISTORY FUNCTIONS ----------
    
    def save_scan(self, user_id, disease_id, image_path, confidence_score):
        """Save a scan to history"""
        query = """
            INSERT INTO SCAN_HISTORY (user_id, disease_id, image_path, confidence_score)
            VALUES (%s, %s, %s, %s)
        """
        params = (user_id, disease_id, image_path, confidence_score)
        
        result = self.execute_query(query, params)
        if result:
            return {"success": True, "message": "Scan saved successfully"}
        return {"success": False, "message": "Failed to save scan"}
    
    def get_user_scans(self, user_id):
        """Get all scans for a user"""
        query = """
            SELECT sh.*, d.disease_name, d.symptoms, d.cause
            FROM SCAN_HISTORY sh
            JOIN DISEASES d ON sh.disease_id = d.disease_id
            WHERE sh.user_id = %s
            ORDER BY sh.scan_date DESC
        """
        return self.execute_query(query, (user_id,)) or []
    
    def get_scan_by_id(self, scan_id):
        """Get a specific scan by ID"""
        query = """
            SELECT sh.*, d.disease_name, d.symptoms, d.cause, d.description,
                   t.treatment, t.prevention
            FROM SCAN_HISTORY sh
            JOIN DISEASES d ON sh.disease_id = d.disease_id
            LEFT JOIN TREATMENTS t ON d.disease_id = t.disease_id
            WHERE sh.scan_id = %s
        """
        result = self.execute_query(query, (scan_id,))
        if result and len(result) > 0:
            return result[0]
        return None