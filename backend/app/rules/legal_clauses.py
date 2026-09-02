import re

MANDATORY_RULES = [
    {
        "rule_id": "R1",
        "rule_name": "Name & Address of Manufacturer/Packer/Importer",
        "section": "Rule 6(1)(a)",
        "description": "Every package must declare the name and complete address of the manufacturer, packer, or importer.",
        "patterns": [
            r"(?i)(manufactur|packer|import|packed\s*by|made\s*by|mfg\.?\s*by|mfd\.?\s*by|marketed\s*by)",
            r"(?i)(address|city|state|pin\s*code|pincode|\b\d{6}\b)"
        ],
        "keywords": ["manufacturer", "packer", "importer", "packed by", "made by", "mfg by", "mfd by"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R2",
        "rule_name": "Net Quantity Declaration",
        "section": "Rule 6(1)(b)",
        "description": "Declaration of net quantity in standard units of weight, measure or number.",
        "patterns": [
            r"(?i)(net\s*(wt\.?|weight|qty\.?|quantity|content))",
            r"(?i)\b\d+(\.\d+)?\s*(g|gm|kg|ml|l|ltr|pieces|pcs)\b"
        ],
        "keywords": ["net wt", "weight", "qty", "quantity", "content"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R3",
        "rule_name": "Maximum Retail Price (MRP)",
        "section": "Rule 6(1)(c)",
        "description": "Retail sale price of the package shall clearly indicate that it is the maximum retail price inclusive of all taxes.",
        "patterns": [
            r"(?i)(m\.?r\.?p\.?|maximum\s*retail\s*price|retail\s*price)",
            r"(?i)(rs\.?|₹|inr)\s*\d+",
            r"(?i)(incl(\.|usive)?\s*of\s*all\s*taxes|incl\.?\s*all\s*taxes)"
        ],
        "keywords": ["MRP", "maximum retail price", "inclusive of all taxes", "Rs", "₹"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R4",
        "rule_name": "Date of Manufacture/Packing/Import",
        "section": "Rule 6(1)(d)",
        "description": "The month and year in which the commodity is manufactured or pre-packed or imported.",
        "patterns": [
            r"(?i)(mfg\.?\s*d(ate|t)?|mfd\.?\s*d(ate|t)?|date\s*of\s*mfg|pkd|packed)",
            r"(?i)(best\s*before|use\s*by|exp(iry)?\.?\s*d(ate|t)?|bb)",
            r"(?i)(\d{2}[/\-.]\d{2}[/\-.]\d{2,4}|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b)"
        ],
        "keywords": ["mfg date", "mfd", "best before", "expiry", "use by"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R5",
        "rule_name": "Consumer Care Details",
        "section": "Rule 6(1)(e)",
        "description": "Name, address, telephone number, e-mail address of the person who can be or the office which can be contacted, in case of consumer complaints.",
        "patterns": [
            r"(?i)(consumer\s*care|customer\s*care|helpline|toll\s*free|feedback|complaint)",
            r"(?i)(1800[-\s]?\d{3}[-\s]?\d{4}|\b\d{10}\b|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
        ],
        "keywords": ["consumer care", "customer care", "helpline", "toll free", "email"],
        "severity": "MEDIUM"
    },
    {
        "rule_id": "R6",
        "rule_name": "Common/Generic Name of Commodity",
        "section": "Rule 6(1)(f)",
        "description": "The name of the commodity contained in the package.",
        "patterns": [
            r"(?i)(product|commodity|ingredient|composition|content|material)"
        ],
        "keywords": ["product", "commodity", "ingredient", "composition", "content"],
        "severity": "MEDIUM"
    }
]

def get_all_rules():
    """
    Returns the list of all mandatory legal clauses.
    """
    return MANDATORY_RULES

def match_rule(rule, text):
    """
    Runs all regex patterns for a given rule against the provided text.
    Returns a dictionary containing the match status and details.
    """
    matched_snippets = []
    
    for pattern in rule["patterns"]:
        matches = re.finditer(pattern, text)
        for match in matches:
            snippet = match.group(0).strip()
            if snippet not in matched_snippets:
                matched_snippets.append(snippet)
                if len(matched_snippets) >= 5:
                    break
        if len(matched_snippets) >= 5:
            break

    is_present = len(matched_snippets) > 0

    return {
        "rule_id": rule["rule_id"],
        "rule_name": rule["rule_name"],
        "section": rule["section"],
        "is_present": is_present,
        "matched_patterns_count": len(matched_snippets),
        "matched_snippets": matched_snippets[:5],
        "severity": rule["severity"]
    }
