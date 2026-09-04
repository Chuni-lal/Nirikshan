import re

MANDATORY_RULES = [
    {
        "rule_id": "R1",
        "rule_name": "Name & Complete Address of Manufacturer/Packer/Importer",
        "section": "Rule 6(1)(a)",
        "description": "Every package must declare the name and complete address of the manufacturer, packer, or importer.",
        "patterns": [
            r"(?i)(manufactur\w*|packer\w*|importer\w*|packed\s*by|made\s*by|mfg\.?\s*by|mfd\.?\s*by|mktd\.?\s*by|marketed\s*by|distributed\s*by|lic\s*no|fssai)[^\n,.]*",
            r"(?i)(address|regd\.?\s*office|factory|city|state|pincode|pin\s*code|\b\d{6}\b|pvt\.?\s*ltd|ltd|inc|corp|building|survey|dist|gujarat|mumbai|delhi|bangalore|india)"
        ],
        "keywords": ["manufacturer", "packer", "importer", "packed by", "made by", "mfg by", "mfd by", "marketed by", "address", "pincode"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R2",
        "rule_name": "Net Quantity / Measure Declaration",
        "section": "Rule 6(1)(b)",
        "description": "Declaration of net quantity in standard metric units of weight, measure or number.",
        "patterns": [
            r"(?i)(net\s*(wt\.?|weight|qty\.?|quantity|content|vol\.?|volume)|contents|n\.?w\.?)\s*[:.-]?\s*\d+(\.\d+)?\s*(g|gm|gms|gram|grams|kg|kgs|ml|mL|ML|l|L|ltr|liter|litres|pcs|pieces|units|u|n|nos|pack)\b",
            r"(?i)\b\d+(\.\d+)?\s*(g|gm|gms|gram|grams|kg|kgs|ml|mL|ML|l|L|ltr|liter|litres|pcs|pieces|units|pack)\b"
        ],
        "keywords": ["net wt", "net weight", "net qty", "net quantity", "net vol", "net content", "net volume"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R3",
        "rule_name": "Maximum Retail Price (MRP inclusive of all taxes)",
        "section": "Rule 6(1)(e)",
        "description": "Retail sale price of the package indicating Maximum Retail Price inclusive of all taxes.",
        "patterns": [
            r"(?i)(m\.?r\.?p\.?|maximum\s*retail\s*price|retail\s*price|max\.?\s*retail\s*price)\s*[:.]?\s*(rs\.?|₹|inr|re\.?)?\s*[:.]?\s*\d+([\.,]\d{1,2})?(\/-)?\s*([(\[]?\s*incl(\.|usive)?\s*of\s*all\s*taxes[)\]]?)?",
            r"(?i)(rs\.?|₹|inr)\s*[:.]?\s*\d+([\.,]\d{1,2})?(\/-)?\s*([(\[]?\s*incl(\.|usive)?\s*of\s*all\s*taxes[)\]]?)?",
            r"(?i)(incl(\.|usive)?\s*of\s*all\s*taxes|incl\.?\s*all\s*taxes)"
        ],
        "keywords": ["maximum retail price", "retail price", "mrp", "incl. of all taxes", "inclusive of all taxes"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R4",
        "rule_name": "Month & Year of Manufacture / Packing / Expiry",
        "section": "Rule 6(1)(d)",
        "description": "The month and year in which the commodity is manufactured, packed or imported, or expiry date.",
        "patterns": [
            r"(?i)(mfg\.?\s*d(ate|t)?|mfd\.?\s*d(ate|t)?|date\s*of\s*mfg|pkd|packed|dom|dop|exp(iry)?\.?\s*d(ate|t)?|best\s*before|use\s*by|bb|batch|b\.?no|lot)\s*[:.]?\s*[a-z0-9/\-. ]+",
            r"(?i)(\d{1,2}[/\-.]\d{2,4}|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*['\s\-/.]*\d{2,4}\b|\b\d{1,2}\s*months?\b)"
        ],
        "keywords": ["mfg date", "mfd date", "date of mfg", "best before", "expiry date", "exp date", "use by", "pkd"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R5",
        "rule_name": "Country of Origin",
        "section": "Rule 6(1)(f)",
        "description": "Country of origin for imported or domestically packaged commodities.",
        "patterns": [
            r"(?i)(country\s*of\s*origin|made\s*in|origin|product\s*of|domestically\s*packaged)\s*[:.]?\s*[a-z ]+",
            r"(?i)(made\s*in\s*india|product\s*of\s*india|country\s*of\s*origin\s*[:.]?\s*india|assembled\s*in\s*india)"
        ],
        "keywords": ["country of origin", "made in india", "product of india", "origin india"],
        "severity": "HIGH"
    },
    {
        "rule_id": "R6",
        "rule_name": "Consumer Care Details",
        "section": "Rule 6(1)(g)",
        "description": "Name, address, telephone number, e-mail address of the person/office for consumer complaints.",
        "patterns": [
            r"(?i)(consumer\s*care|customer\s*care|helpline|toll\s*free|feedback|complaint|care\s*no|contact|write\s*to)\s*[:.]?\s*[a-z0-9@._+\- ]+",
            r"(?i)(1800[-\s]?\d{3}[-\s]?\d{4}|\b\d{10}\b|\+?91[-\s]?\d{10}\b|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
        ],
        "keywords": ["consumer care", "customer care", "helpline", "toll free", "care no", "email", "customer care no"],
        "severity": "MEDIUM"
    }
]

def get_all_rules():
    return MANDATORY_RULES

def match_rule(rule, full_text):
    """
    Runs pattern matching and keyword extraction for a given rule against full OCR text.
    Extracts complete statutory declaration snippets.
    """
    matched_snippets = []
    
    # 1. Regex Pattern Matching
    for pattern in rule["patterns"]:
        matches = re.finditer(pattern, full_text)
        for match in matches:
            snippet = match.group(0).strip()
            if snippet and len(snippet) >= 3 and snippet not in matched_snippets:
                matched_snippets.append(snippet)
                if len(matched_snippets) >= 5:
                    break
        if len(matched_snippets) >= 5:
            break

    # 2. Keyword Fallback Matching (multi-word keywords only to avoid single-letter noise)
    if not matched_snippets and "keywords" in rule:
        text_lower = full_text.lower()
        for kw in rule["keywords"]:
            if len(kw) >= 3 and kw.lower() in text_lower:
                idx = text_lower.find(kw.lower())
                context_snippet = full_text[max(0, idx - 5): min(len(full_text), idx + len(kw) + 35)].strip()
                if context_snippet and context_snippet not in matched_snippets:
                    matched_snippets.append(context_snippet)
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

def parse_structured_declarations(full_text: str) -> dict:
    """
    Parses and extracts exact clean structured key-value declarations:
    - MRP amount (e.g. 'Rs. 150.00 (Incl. of all taxes)')
    - Net Quantity (e.g. '500 g')
    - Manufacturing / Expiry Date (e.g. '04/2026')
    - Manufacturer Details
    - Consumer Care Contact
    - Country of Origin
    """
    declarations = {
        "mrp": "NOT DETECTED",
        "net_quantity": "NOT DETECTED",
        "mfg_date": "NOT DETECTED",
        "manufacturer": "NOT DETECTED",
        "country_of_origin": "NOT DETECTED",
        "consumer_care": "NOT DETECTED"
    }

    # 1. Exact MRP Extraction
    mrp_match = re.search(r"(?i)(m\.?r\.?p\.?|maximum\s*retail\s*price)\s*[:.]?\s*(rs\.?|₹|inr)?\s*[:.]?\s*(\d+([\.,]\d{1,2})?(\/-)?)\s*([(\[]?\s*incl(\.|usive)?\s*of\s*all\s*taxes[)\]]?)?", full_text)
    if mrp_match:
        declarations["mrp"] = mrp_match.group(0).strip()
    else:
        mrp_fallback = re.search(r"(?i)(rs\.?|₹|inr)\s*[:.]?\s*\d+([\.,]\d{1,2})?(\/-)?", full_text)
        if mrp_fallback:
            declarations["mrp"] = mrp_fallback.group(0).strip()

    # 2. Exact Net Quantity Extraction
    net_match = re.search(r"(?i)(net\s*(wt\.?|weight|qty\.?|quantity|content|vol\.?|volume))\s*[:.-]?\s*\d+(\.\d+)?\s*(g|gm|gms|gram|grams|kg|kgs|ml|mL|ML|l|L|ltr|liter|litres|pcs|pieces|units|u|n|nos|pack)\b", full_text)
    if net_match:
        declarations["net_quantity"] = net_match.group(0).strip()
    else:
        net_fallback = re.search(r"(?i)\b\d+(\.\d+)?\s*(g|gm|gms|gram|grams|kg|kgs|ml|mL|ML|l|L|ltr|liter|litres|pcs|pieces|pack)\b", full_text)
        if net_fallback:
            declarations["net_quantity"] = net_fallback.group(0).strip()

    # 3. Exact Manufacturing / Expiry Date Extraction
    date_match = re.search(r"(?i)(mfg\.?\s*d(ate|t)?|mfd\.?\s*d(ate|t)?|date\s*of\s*mfg|pkd|packed|exp(iry)?\.?\s*d(ate|t)?|best\s*before|use\s*by)\s*[:.]?\s*[a-z0-9/\-. ]+", full_text)
    if date_match:
        declarations["mfg_date"] = date_match.group(0).strip()
    else:
        date_fallback = re.search(r"(?i)(\d{1,2}[/\-.]\d{2,4}|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*['\s\-/.]*\d{2,4}\b)", full_text)
        if date_fallback:
            declarations["mfg_date"] = date_fallback.group(0).strip()

    # 4. Manufacturer Details
    mfr_match = re.search(r"(?i)(manufactur\w*|packer\w*|importer\w*|packed\s*by|made\s*by|mfg\.?\s*by|mfd\.?\s*by|mktd\.?\s*by|marketed\s*by)[^\n,.]*", full_text)
    if mfr_match:
        declarations["manufacturer"] = mfr_match.group(0).strip()

    # 5. Country of Origin
    origin_match = re.search(r"(?i)(made\s*in\s*india|product\s*of\s*india|country\s*of\s*origin\s*[:.]?\s*india)", full_text)
    if origin_match:
        declarations["country_of_origin"] = origin_match.group(0).strip()

    # 6. Consumer Care
    care_match = re.search(r"(?i)(consumer\s*care|customer\s*care|helpline|toll\s*free|care\s*no)[^\n]*", full_text)
    if care_match:
        declarations["consumer_care"] = care_match.group(0).strip()

    return declarations
