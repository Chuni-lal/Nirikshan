from typing import List, Dict, Any
from .legal_clauses import get_all_rules, match_rule

def evaluate_compliance(ocr_results: List[Dict[str, Any]], font_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates compliance against legal metrology rules and font size requirements.
    
    Args:
        ocr_results (list): Output from OCR engine containing extracted text.
        font_analysis (list): Output from font analyzer containing font sizes and compliance.
        
    Returns:
        dict: Full compliance report.
    """
    # Phase 1: Rule Presence Check
    extracted_text = " ".join([item.get("text", "") for item in ocr_results])
    
    rules = get_all_rules()
    rule_results = []
    violations = []
    
    rules_passed = 0
    rules_failed = 0
    
    for rule in rules:
        result = match_rule(rule, extracted_text)
        result["status"] = "PASS" if result["is_present"] else "FAIL"
        
        if result["status"] == "PASS":
            rules_passed += 1
        else:
            rules_failed += 1
            violations.append({
                "rule_id": rule["rule_id"],
                "rule_name": rule["rule_name"],
                "description": rule["description"],
                "severity": rule["severity"]
            })
            
        rule_results.append(result)
        
    # Phase 2: Font Size Check
    font_violations = []
    font_compliant_count = 0
    font_non_compliant_count = 0
    
    for font_item in font_analysis:
        if font_item.get("is_compliant", True):
            font_compliant_count += 1
        else:
            font_non_compliant_count += 1
            font_violations.append({
                "text": font_item.get("text", ""),
                "font_size_mm": font_item.get("font_size_mm", 0.0),
                "min_required_mm": font_item.get("min_required_mm", 0.0)
            })
            
    total_rules_checked = len(rules)
    
    overall_status = "COMPLIANT" if (rules_failed == 0 and len(font_violations) == 0) else "NON-COMPLIANT"
    
    return {
        "overall_status": overall_status,
        "total_rules_checked": total_rules_checked,
        "rules_passed": rules_passed,
        "rules_failed": rules_failed,
        "rule_results": rule_results,
        "violations": violations,
        "font_violations": font_violations,
        "extracted_text": extracted_text,
        "total_text_blocks": len(ocr_results),
        "font_analysis_summary": {
            "total_analyzed": len(font_analysis),
            "compliant": font_compliant_count,
            "non_compliant": font_non_compliant_count
        }
    }
