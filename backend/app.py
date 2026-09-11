# backend/app.py
# Flask Backend for PhytoDx

from flask import Flask, request, jsonify
from flask_cors import CORS
from db import Database

# Create Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

# Create database object
db = Database()

# ---------- HOME ROUTE ----------
@app.route('/')
def home():
    """Test if API is running"""
    return jsonify({"message": "PhotoDx API is running!"})

# ---------- REGISTER ROUTE ----------
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', '')
        
        if not name or not email or not password:
            return jsonify({
                "success": False,
                "message": "Name, email and password are required"
            }), 400
        
        db.connect()
        result = db.register_user(name, email, password, phone)
        db.disconnect()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# ---------- LOGIN ROUTE ----------
@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400
        
        db.connect()
        result = db.login_user(email, password)
        db.disconnect()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# ---------- GET ALL DISEASES ROUTE ----------
@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get all diseases"""
    try:
        db.connect()
        diseases = db.get_all_diseases()
        db.disconnect()
        
        return jsonify({
            "success": True,
            "diseases": diseases
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# ---------- GET DISEASE BY NAME ROUTE ----------
@app.route('/api/disease/<string:disease_name>', methods=['GET'])
def get_disease_by_name(disease_name):
    """Get disease details with treatment by name"""
    try:
        db.connect()
        disease_info = db.get_disease_with_treatment(disease_name)
        db.disconnect()
        
        if disease_info:
            return jsonify({
                "success": True,
                "disease": disease_info
            })
        else:
            return jsonify({
                "success": False,
                "message": "Disease not found"
            }), 404
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# ---------- SAVE SCAN HISTORY ROUTE ----------
@app.route('/api/save_scan', methods=['POST'])
def save_scan():
    """Save scan result to history"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        disease_name = data.get('disease_name')
        confidence = data.get('confidence')
        image_path = data.get('image_path', '')
        
        if not user_id or not disease_name:
            return jsonify({
                "success": False,
                "message": "User ID and disease name are required"
            }), 400
        
        db.connect()
        
        # Get disease ID from disease name
        disease = db.get_disease_by_name(disease_name)
        if not disease:
            # If disease not found, create a new entry
            query = "INSERT INTO DISEASES (disease_name) VALUES (%s)"
            db.execute_query(query, (disease_name,))
            # Get the new disease ID
            disease = db.get_disease_by_name(disease_name)
            disease_id = disease['disease_id'] if disease else None
        else:
            disease_id = disease['disease_id']
        
        if not disease_id:
            db.disconnect()
            return jsonify({
                "success": False,
                "message": "Could not find or create disease"
            }), 500
        
        # Save scan
        result = db.save_scan(user_id, disease_id, image_path, confidence)
        db.disconnect()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# ---------- GET USER SCANS ROUTE ----------
@app.route('/api/get_scans/<int:user_id>', methods=['GET'])
def get_scans(user_id):
    """Get all scans for a user"""
    try:
        db.connect()
        scans = db.get_user_scans(user_id)
        db.disconnect()
        
        return jsonify({
            "success": True,
            "scans": scans
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# ---------- RUN THE APP ----------
if __name__ == '__main__':
    app.run(debug=True, port=5000)