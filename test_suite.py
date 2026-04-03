import sqlite3
import hashlib
import json
import os
import requests
import time
from config import DB_PATH, SECRET_SALT

def test_db_crud():
    print("\n--- Testing Database CRUD ---")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 1. Create (Insert)
        name = "Test Patient"
        aadhaar = "123412341234"
        salted = f"{aadhaar}{SECRET_SALT}"
        h = hashlib.sha256(salted.encode()).hexdigest()
        
        c.execute("INSERT INTO patients (name, age, gender, aadhaar_hash, registration_type) VALUES (?, ?, ?, ?, ?)",
                  (name, 30, "Male", h, "Temporary"))
        p_id = c.lastrowid
        print(f"Created Patient ID: {p_id}")
        
        # 2. Read
        c.execute("SELECT name FROM patients WHERE patient_id = ?", (p_id,))
        fetched_name = c.fetchone()[0]
        assert fetched_name == name, "Name mismatch!"
        print(f"Read Patient Name: {fetched_name}")
        
        # 3. Update
        new_name = "Updated Patient"
        c.execute("UPDATE patients SET name = ? WHERE patient_id = ?", (new_name, p_id))
        conn.commit()
        
        c.execute("SELECT name FROM patients WHERE patient_id = ?", (p_id,))
        fetched_new_name = c.fetchone()[0]
        assert fetched_new_name == new_name, "Update failed!"
        print(f"Updated Patient Name: {fetched_new_name}")
        
        # 4. Delete
        c.execute("DELETE FROM patients WHERE patient_id = ?", (p_id,))
        conn.commit()
        c.execute("SELECT COUNT(*) FROM patients WHERE patient_id = ?", (p_id,))
        count = c.fetchone()[0]
        assert count == 0, "Delete failed!"
        print("Delete Patient: Successful")
        
        conn.close()
        return True
    except Exception as e:
        print(f"DB Test Error: {e}")
        return False

def test_admin_api():
    print("\n--- Testing Admin API Endpoints ---")
    base_url = "http://localhost:8080/api"
    
    try:
        # Check if server is running
        try:
            requests.get(f"{base_url}/status", timeout=2)
        except:
            print("ERROR: Admin Server is NOT running. Start it first with 'python main.py'")
            return False

        # 1. Test Stats
        r = requests.get(f"{base_url}/stats")
        assert r.status_code == 200, "Stats API failed"
        print("API Stats: OK")
        
        # 2. Test Recent
        r = requests.get(f"{base_url}/recent")
        assert r.status_code == 200, "Recent API failed"
        print("API Recent: OK")
        
        # 3. Test Detail (Requires Auth)
        # Note: We can't easily test auth-protected APIs without a session
        print("API Auth: (Manual Check Required via Browser)")
        
        return True
    except Exception as e:
        print(f"API Test Error: {e}")
        return False

if __name__ == "__main__":
    db_success = test_db_crud()
    api_success = test_admin_api()
    
    if db_success and api_success:
        print("\n--- ALL CORE TESTS PASSED ---")
    else:
        print("\n--- SOME TESTS FAILED ---")
