# ─────────────────────────────────────────────────────────────────
# services/admin_server.py — Admin Dashboard API & Static Server
# ─────────────────────────────────────────────────────────────────

import os
import json
import sqlite3
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from config import DB_PATH, ADMIN_PASSWORD
from utils.logger import get_logger

log = get_logger("services.admin")

class AdminHandler(BaseHTTPRequestHandler):
    """Handles API requests and serves the dashboard HTML."""
    # ── Admin State (Static) ───────────────────────
    is_authenticated = False
    admin_password = ADMIN_PASSWORD
    kiosk_online = True

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        # 1. API: Login
        if self.path == "/api/login":
            if post_data.get("password") == self.admin_password:
                AdminHandler.is_authenticated = True
                self._send_json({"success": True})
            else:
                self._send_json({"success": False, "message": "Invalid password"}, status=401)

        # 2. API: Toggle Kiosk
        elif self.path == "/api/toggle_kiosk":
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False}, status=403)
                return
            AdminHandler.kiosk_online = post_data.get("online", True)
            log.info(f"Kiosk status changed: {'ONLINE' if AdminHandler.kiosk_online else 'OFFLINE'}")
            self._send_json({"success": True, "online": AdminHandler.kiosk_online})

        # 3. API: Check-in Patient
        elif self.path.startswith("/api/checkin"):
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False}, status=403)
                return
            
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            patient_id = params.get('id', [None])[0]
            
            if patient_id:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    # Update status for the LATEST token of this patient
                    c.execute("UPDATE tokens SET status = 'checked' WHERE patient_id = ? AND token_id = (SELECT MAX(token_id) FROM tokens WHERE patient_id = ?)", (patient_id, patient_id))
                    conn.commit()
                    conn.close()
                    self._send_json({"success": True})
                except Exception as e:
                    log.error(f"Check-in Error: {e}")
                    self._send_json({"success": False}, status=500)
            else:
                self._send_json({"success": False}, status=400)

        # 4. API: Save Settings
        elif self.path == "/api/settings":
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False}, status=403)
                return
            log.info(f"Settings updated: {post_data}")
            self._send_json({"success": True})

        # 4b. API: Update Patient Detail
        elif self.path == "/api/update_patient":
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False}, status=403)
                return
            self._send_json(self._update_patient(post_data))

        # 5. API: Submit Patient Feedback
        elif self.path == "/api/feedback":
            # Public endpoint (no auth needed)
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("INSERT INTO feedback (rating, comments) VALUES (?, ?)", 
                         (post_data.get("rating", 5), post_data.get("comments", "")))
                conn.commit()
                conn.close()
                self._send_json({"success": True})
            except Exception as e:
                log.error(f"Feedback Error: {e}")
                self._send_json({"success": False}, status=500)

    def do_GET(self):
        import urllib.parse
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        # 1. API: Get Current Stats
        if path == "/api/stats" or path == "/api/v1/stats":
            self._send_json(self._get_db_stats())

        # 1b. API: Auth Check
        elif path == "/api/auth_check":
            if AdminHandler.is_authenticated:
                self._send_json({"authenticated": True})
            else:
                self._send_json({"authenticated": False}, status=401)

        # 2. API: Get Recent Patients (History) with Advanced Sort/Filter
        elif path == "/api/recent" or path == "/api/v1/recent":
            sort_key = params.get('sort', ['id_desc'])[0]
            filter_val = params.get('filter', [None])[0]
            limit_val = int(params.get('limit', [50])[0])
            
            self._send_json(self._get_db_recent(sort_key, filter_val, limit_val))
            
        # 3. API: Get Settings & Kiosk Status
        elif path == "/api/status" or path == "/api/v1/status":
            self._send_json({"online": AdminHandler.kiosk_online, "hospital": "Smart Care Hospital"})

        # 3b. API: Get Full Patient Detail
        elif path == "/api/patient_detail" or path == "/api/v1/patient_detail":
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False, "message": "Unauthorized"}, status=403)
                return
            
            p_id = params.get('id', [None])[0]
            if p_id:
                detail = self._get_db_patient_detail(p_id)
                if detail:
                    self._send_json(detail)
                else:
                    self._send_json({"success": False, "message": "Patient not found"}, status=404)
            else:
                self._send_json({"success": False}, status=400)

        # 3c. API: Delete Patient
        elif path == "/api/delete_patient":
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False}, status=403)
                return
            p_id = params.get('id', [None])[0]
            if p_id:
                self._send_json(self._delete_patient(p_id))
            else:
                self._send_json({"success": False}, status=400)

        # 3d. API: Clear All Data
        elif path == "/api/clear_all_data":
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False}, status=403)
                return
            self._send_json(self._clear_all_db_data())

        # 4. API: Get Patient Feedback
        elif path == "/api/feedback":
            if not AdminHandler.is_authenticated:
                self._send_json({"success": False}, status=403)
                return
            self._send_json(self._get_db_feedback())

        # 5. Static: Serve Dashboard HTML
        elif path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_path = os.path.join("assets", "admin", "index.html")
            if os.path.exists(html_path):
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>Admin Dashboard File Missing</h1>")
        else:
            self.send_error(404, "Not Found")

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_db_stats(self):
        """Fetch total patient and emergency case counts."""
        try:
            conn = sqlite3.connect(DB_PATH)
            c    = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM patients")
            total = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM tokens WHERE is_emergency = 1")
            emergency = c.fetchone()[0]
            
            c.execute("SELECT AVG(temperature) FROM health_records")
            avg_temp = c.fetchone()[0] or 0.0
            
            conn.close()
            return {
                "total": total,
                "emergency": emergency,
                "avg_temp": round(avg_temp, 1)
            }
        except Exception as e:
            log.error(f"DB Error (stats): {e}")
            return {"total": 0, "emergency": 0, "avg_temp": 0.0}

    def _get_db_recent(self, sort_key="id_desc", filter_val=None, limit=50):
        """Fetch details of registrations with advanced sorting and filtering."""
        try:
            conn = sqlite3.connect(DB_PATH)
            c    = conn.cursor()
            
            # Map sort keys to SQL
            sort_map = {
                "id_desc": "p.patient_id DESC",
                "id_asc" : "p.patient_id ASC",
                "name_asc": "p.name ASC",
                "name_desc": "p.name DESC",
                "time_desc": "t.issued_at DESC",
                "time_asc": "t.issued_at ASC",
                "dept_asc": "t.department ASC",
                "dept_desc": "t.department DESC",
                "severity_asc": "t.severity ASC",
                "severity_desc": "t.severity DESC"
            }
            order_by = sort_map.get(sort_key, "p.patient_id DESC")

            # Basic Query
            query = """
                SELECT p.patient_id, p.name, p.registration_type, 
                       t.department, h.temperature, h.heart_rate, t.issued_at, t.severity,
                       (SELECT GROUP_CONCAT(symptom_code) FROM symptoms WHERE patient_id = p.patient_id) as s_list,
                       t.status
                FROM patients p
                LEFT JOIN (SELECT * FROM tokens GROUP BY patient_id HAVING MAX(token_id)) t 
                     ON p.patient_id = t.patient_id
                LEFT JOIN (SELECT * FROM health_records GROUP BY patient_id HAVING MAX(record_id)) h 
                     ON p.patient_id = h.patient_id
            """
            
            # Add filtering if needed
            if filter_val:
                # filter_val could be a comma-separated list of symptoms or departments
                filters = filter_val.split(',')
                filter_clauses = []
                for f in filters:
                    f = f.strip()
                    if f:
                        # We use the subquery directly in WHERE to avoid alias issues in some SQLite versions
                        filter_clauses.append(f"(t.department LIKE '%{f}%' OR (SELECT GROUP_CONCAT(symptom_code) FROM symptoms WHERE patient_id = p.patient_id) LIKE '%{f}%')")
                
                if filter_clauses:
                    query += " WHERE (" + " OR ".join(filter_clauses) + ")"

            query += f" ORDER BY {order_by} LIMIT {limit}"
            
            c.execute(query)
            rows = c.fetchall()
            conn.close()

            results = []
            for r in rows:
                results.append({
                    "id": r[0], "name": r[1], "type": r[2],
                    "department": r[3] or "N/A", "temp": r[4] or "--",
                    "hr": r[5] or "--", "time": r[6] or "--", "severity": r[7] or "Normal",
                    "symptoms": r[8] or "", "status": r[9] or "waiting"
                })
            return results
        except Exception as e:
            log.error(f"DB Error (recent): {e}")
            return []

    def _get_db_patient_detail(self, patient_id):
        """Fetch full profile of a specific patient."""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                SELECT p.patient_id, p.name, p.age, p.gender, p.registration_type, 
                       p.allergies, p.medical_history, p.created_at,
                       t.department, t.doctor_type, t.severity, t.token_number, t.status,
                       h.temperature, h.heart_rate, h.spo2, h.amb_temp, h.humidity
                FROM patients p
                LEFT JOIN tokens t ON p.patient_id = t.patient_id
                LEFT JOIN health_records h ON p.patient_id = h.patient_id
                WHERE p.patient_id = ?
                ORDER BY t.token_id DESC, h.record_id DESC LIMIT 1
            """, (patient_id,))
            r = c.fetchone()
            conn.close()
            
            if r:
                return {
                    "id": r[0], "name": r[1], "age": r[2], "gender": r[3], "type": r[4],
                    "allergies": r[5] or "None", "history": r[6] or "None", "created": r[7],
                    "dept": r[8], "doctor": r[9], "severity": r[10], "token": r[11], "status": r[12],
                    "vitals": {"temp": r[13], "hr": r[14], "spo2": r[15], "amb": r[16], "hum": r[17]},
                    "aadhaar_hash": r[0] # Just returning ID as placeholder for "Aadhaar info available"
                }
            return None
        except Exception as e:
            log.error(f"DB Error (detail): {e}")
            return None

    def _update_patient(self, data):
        """Update patient profile and latest health/token records."""
        try:
            p_id = data.get("id")
            if not p_id: return {"success": False}
            
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # 1. Update Patient Table
            c.execute("""
                UPDATE patients 
                SET name = ?, age = ?, gender = ?, registration_type = ?, allergies = ?, medical_history = ?
                WHERE patient_id = ?
            """, (data.get("name"), data.get("age"), data.get("gender"), data.get("type"), 
                  data.get("allergies"), data.get("history"), p_id))
            
            # 2. Update Latest Health Record
            c.execute("""
                UPDATE health_records 
                SET temperature = ?, heart_rate = ?, spo2 = ?
                WHERE patient_id = ? AND record_id = (SELECT MAX(record_id) FROM health_records WHERE patient_id = ?)
            """, (data.get("temp"), data.get("hr"), data.get("spo2"), p_id, p_id))
            
            # 3. Update Latest Token
            c.execute("""
                UPDATE tokens 
                SET department = ?, severity = ?
                WHERE patient_id = ? AND token_id = (SELECT MAX(token_id) FROM tokens WHERE patient_id = ?)
            """, (data.get("dept"), data.get("severity"), p_id, p_id))
            
            conn.commit()
            conn.close()
            return {"success": True}
        except Exception as e:
            log.error(f"DB Update Error: {e}")
            return {"success": False, "error": str(e)}

    def _delete_patient(self, p_id):
        """Delete all records related to a patient."""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM tokens WHERE patient_id = ?", (p_id,))
            c.execute("DELETE FROM health_records WHERE patient_id = ?", (p_id,))
            c.execute("DELETE FROM symptoms WHERE patient_id = ?", (p_id,))
            c.execute("DELETE FROM patients WHERE patient_id = ?", (p_id,))
            conn.commit()
            conn.close()
            return {"success": True}
        except Exception as e:
            log.error(f"DB Delete Error: {e}")
            return {"success": False, "error": str(e)}

    def _clear_all_db_data(self):
        """Wipe all tables permanently."""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM tokens")
            c.execute("DELETE FROM health_records")
            c.execute("DELETE FROM symptoms")
            c.execute("DELETE FROM patients")
            c.execute("DELETE FROM feedback")
            conn.commit()
            conn.close()
            log.warning("ADMIN: All database data cleared permanently.")
            return {"success": True}
        except Exception as e:
            log.error(f"DB Clear Error: {e}")
            return {"success": False, "error": str(e)}

    def _get_db_feedback(self):
        """Fetch all patient feedback records."""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT rating, comments, created_at FROM feedback ORDER BY created_at DESC")
            rows = c.fetchall()
            conn.close()
            return [{"rating": r[0], "comments": r[1], "time": r[2]} for r in rows]
        except Exception as e:
            log.error(f"DB Error (feedback): {e}")
            return []

def start_admin_dashboard(port=8080):
    """Start the admin server in a background thread."""
    server = HTTPServer(('0.0.0.0', port), AdminHandler)
    log.info(f"Admin Dashboard starting at http://localhost:{port}")
    
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server
