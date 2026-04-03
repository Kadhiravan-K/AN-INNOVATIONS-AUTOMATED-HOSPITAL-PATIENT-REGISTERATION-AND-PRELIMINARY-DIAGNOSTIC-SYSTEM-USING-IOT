import sqlite3
import hashlib
import os
from config import DB_PATH, SECRET_SALT

def test_db_crud():
    print("\n--- Testing Database CRUD ---")
    try:
        if not os.path.exists(DB_PATH):
            print(f"ERROR: Database file not found at {DB_PATH}")
            return False
            
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 1. Create (Insert)
        name = "Test Patient Automation"
        aadhaar = "111122223333"
        salted = f"{aadhaar}{SECRET_SALT}"
        h = hashlib.sha256(salted.encode()).hexdigest()
        
        c.execute("INSERT INTO patients (name, age, gender, aadhaar_hash, registration_type) VALUES (?, ?, ?, ?, ?)",
                  (name, 45, "Female", h, "Permanent"))
        p_id = c.lastrowid
        print(f"SUCCESS: Created Patient ID: {p_id}")
        
        # 2. Read
        c.execute("SELECT name, registration_type FROM patients WHERE patient_id = ?", (p_id,))
        row = c.fetchone()
        assert row[0] == name, "Name mismatch!"
        assert row[1] == "Permanent", "Type mismatch!"
        print(f"SUCCESS: Verified Patient Data: {row[0]} ({row[1]})")
        
        # 3. Update
        new_age = 46
        c.execute("UPDATE patients SET age = ? WHERE patient_id = ?", (new_age, p_id))
        conn.commit()
        
        c.execute("SELECT age FROM patients WHERE patient_id = ?", (p_id,))
        fetched_age = c.fetchone()[0]
        assert fetched_age == new_age, "Update failed!"
        print(f"SUCCESS: Updated Patient Age: {fetched_age}")
        
        # 4. Delete
        c.execute("DELETE FROM patients WHERE patient_id = ?", (p_id,))
        conn.commit()
        c.execute("SELECT COUNT(*) FROM patients WHERE patient_id = ?", (p_id,))
        count = c.fetchone()[0]
        assert count == 0, "Delete failed!"
        print("SUCCESS: Deleted Test Record Cleanly")
        
        conn.close()
        return True
    except Exception as e:
        print(f"FAIL: Database Test Error: {e}")
        return False

if __name__ == "__main__":
    success = test_db_crud()
    if success:
        print("\n--- DATABASE INTEGRITY TEST PASSED ---")
    else:
        print("\n--- DATABASE INTEGRITY TEST FAILED ---")
        exit(1)
