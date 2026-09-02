import csv
import json
import os
from typing import List, Dict, Any

def generate_csv_export(records: List[Dict[str, Any]], output_path: str):
    """
    Generates a CSV export of scan records.
    
    Args:
        records (list): List of scan records from the database.
        output_path (str): The destination file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    headers = [
        "Scan ID", "Timestamp", "Filename", "Overall Status", 
        "Rules Checked", "Rules Passed", "Rules Failed", 
        "Violations", "Extracted Text"
    ]
    
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for record in records:
            # Parse violations from JSON if it's a string
            violations_raw = record.get("violations", "[]")
            if isinstance(violations_raw, str):
                try:
                    violations_list = json.loads(violations_raw)
                except json.JSONDecodeError:
                    violations_list = []
            else:
                violations_list = violations_raw
                
            # Extract rule descriptions or names to join
            v_strings = []
            for v in violations_list:
                if isinstance(v, dict):
                    name = v.get("rule_name", "")
                    if name:
                        v_strings.append(name)
                    elif "text" in v:  # Font violation
                        v_strings.append(f"Font violation: {v.get('text')}")
                else:
                    v_strings.append(str(v))
                    
            violations_str = "; ".join(v_strings)
            
            # Truncate extracted text to 200 chars
            extracted_text = record.get("extracted_text", "")
            if extracted_text and len(extracted_text) > 200:
                extracted_text = extracted_text[:197] + "..."
                
            writer.writerow([
                record.get("scan_id", ""),
                record.get("timestamp", ""),
                record.get("filename", ""),
                record.get("overall_status", ""),
                record.get("total_rules_checked", 0),
                record.get("rules_passed", 0),
                record.get("rules_failed", 0),
                violations_str,
                extracted_text
            ])
