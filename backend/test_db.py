# backend/test_db.py
# This file tests the database connection and operations

from db import Database

def test_connection():
    """Test database connection"""
    print("\n=== Testing Database Connection ===\n")
    db = Database()
    
    # Test connection
    if db.connect():
        print("✅ Connection test passed!")
        
        # Test getting all diseases
        print("\n--- Diseases in database ---")
        diseases = db.get_all_diseases()
        for disease in diseases:
            print(f"  • {disease['disease_name']}")
        
        # Test getting user (should be None initially)
        print("\n--- Testing user operations ---")
        user = db.get_user_by_email("test@example.com")
        if user:
            print(f"  User found: {user['name']}")
        else:
            print("  No user found (expected)")
        
        # Test registration
        print("\n--- Testing registration ---")
        result = db.register_user(
            name="Test User",
            email="test@example.com",
            password="password123",
            phone="1234567890"
        )
        print(f"  Registration result: {result['message']}")
        
        # Test login
        print("\n--- Testing login ---")
        result = db.login_user("test@example.com", "password123")
        if result['success']:
            print(f"  ✅ Login successful! Welcome {result['user']['name']}")
        else:
            print(f"  ❌ Login failed: {result['message']}")
        
        # Test getting disease with treatment
        print("\n--- Testing disease with treatment ---")
        disease_info = db.get_disease_with_treatment("Tomato Early Blight")
        if disease_info:
            print(f"  Disease: {disease_info['disease']['disease_name']}")
            print(f"  Symptoms: {disease_info['disease']['symptoms']}")
            if disease_info['treatment']:
                print(f"  Treatment: {disease_info['treatment']['treatment']}")
        
        # Cleanup: Delete test user
        print("\n--- Cleaning up test data ---")
        db.execute_query("DELETE FROM USERS WHERE email = %s", ("test@example.com",))
        print("  Test user deleted")
        
        db.disconnect()
        print("\n✅ All tests completed!")
    else:
        print("❌ Connection failed! Please check your database credentials.")

if __name__ == "__main__":
    test_connection()