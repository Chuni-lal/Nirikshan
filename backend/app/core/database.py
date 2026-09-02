import sqlite3
import json
import os
from .config import DATABASE_PATH

def get_connection():
    """Returns a SQLite connection with dict-like row factory."""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            filename TEXT NOT NULL,
            overall_status TEXT NOT NULL,
            total_rules_checked INTEGER DEFAULT 0,
            rules_passed INTEGER DEFAULT 0,
            rules_failed INTEGER DEFAULT 0,
            violations TEXT,
            extracted_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_scan_record(scan_id, timestamp, filename, compliance_report):
    """Saves a scan record and its compliance report to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    violations_json = json.dumps(compliance_report.get("violations", []))
    extracted_text = compliance_report.get("extracted_text", "")
    overall_status = compliance_report.get("overall_status", "NON-COMPLIANT")
    total_rules = compliance_report.get("total_rules_checked", 0)
    passed = compliance_report.get("rules_passed", 0)
    failed = compliance_report.get("rules_failed", 0)
    
    cursor.execute('''
        INSERT INTO scan_records (
            scan_id, timestamp, filename, overall_status, 
            total_rules_checked, rules_passed, rules_failed, 
            violations, extracted_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (scan_id, timestamp, filename, overall_status, total_rules, passed, failed, violations_json, extracted_text))
    
    conn.commit()
    conn.close()

def get_all_records():
    """Fetches all past scan records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scan_records ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    records = []
    for row in rows:
        record = dict(row)
        if record.get("violations"):
            record["violations"] = json.loads(record["violations"])
        records.append(record)
    return records
