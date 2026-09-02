# 📋 NIRIKSHAN — Product Requirements Document (PRD)

| Field | Value |
|---|---|
| **Document Version** | 1.0 |
| **Date** | September 2026 |
| **Product Name** | Nirikshan — Packaged Commodity Compliance Auditor |
| **Author** | Team Nirikshan |
| **Status** | Draft — Ready for Review |

---

## 1. Executive Summary

**Nirikshan** is an AI-powered software application that automates compliance verification of packaged commodities under the **Legal Metrology (Packaged Commodities) Rules, 2011**. The system enables enforcement officers to scan product labels via image upload, automatically detect and validate 6 mandatory declarations, verify font size legality, and generate court-ready compliance reports — reducing per-product inspection time from ~15 minutes to under 30 seconds.

### 1.1 Vision Statement

> *"To empower every Legal Metrology enforcement officer with an instant, accurate, and offline-capable compliance auditing tool — transforming manual inspections into a digitized, scalable, and evidence-backed process."*

### 1.2 Value Proposition

| Stakeholder | Current Pain | Nirikshan Solution |
|---|---|---|
| Field Inspectors | Manual reading of labels, handwritten notes, subjective assessment | Automated OCR scan, objective rule evaluation, digital reports |
| Regional Directors | No centralized data, no trend visibility | Dashboard with search, analytics, and export capabilities |
| Judiciary/Courts | Handwritten notices, no photo evidence | Machine-generated PDF with embedded photographic evidence |
| Consumers | Low enforcement coverage allows non-compliant products | Scalable inspections cover more products, improving compliance rates |

---

## 2. Problem Statement

### 2.1 Background

Under the **Legal Metrology Act, 2009** and the **Legal Metrology (Packaged Commodities) Rules, 2011**, every pre-packaged commodity sold in India must bear mandatory declarations including:

- Name and address of manufacturer/packer/importer
- Net quantity in standard units
- Maximum Retail Price (MRP) inclusive of all taxes
- Month and year of manufacture/packing/import
- Consumer care contact details
- Common/generic name of the commodity

These declarations ensure transparency, fair trade practices, and consumer protection.

### 2.2 The Problem

| Dimension | Challenge |
|---|---|
| **Volume** | India has millions of packaged products across retail stores, supermarkets, and e-commerce |
| **Speed** | Manual inspection takes ~15 minutes per product (reading, measuring, noting) |
| **Consistency** | Different inspectors may interpret rules differently, leading to inconsistent enforcement |
| **Scalability** | Limited staff cannot cover the vast number of products in the market |
| **Evidence** | Handwritten inspection notes lack standardization and photographic evidence |
| **Data** | No centralized repository of past inspections for trend analysis or auditing |
| **Font Verification** | Physical font size measurement with rulers is impractical at scale |

### 2.3 Opportunity

A software system capable of **automatically detecting, extracting, and validating mandatory declarations through image and label analysis** can transform compliance enforcement from a manual, time-intensive process into an instant, standardized, and scalable digital workflow.

---

## 3. User Personas

### 3.1 Primary Persona: Field Inspector (Shri Rajesh Kumar)

| Attribute | Detail |
|---|---|
| **Role** | Legal Metrology Field Inspector |
| **Age** | 35-50 |
| **Tech Comfort** | Moderate — uses smartphone and basic desktop applications |
| **Work Environment** | Retail stores, warehouses, markets (often with poor internet) |
| **Key Tasks** | Inspect packaged products, document violations, issue notices |
| **Pain Points** | Manual reading is slow, font measurement is difficult, paper-based reporting |
| **Goals** | Scan products quickly, generate accurate reports, maintain digital records |

### 3.2 Secondary Persona: Regional Director (Dr. Priya Sharma)

| Attribute | Detail |
|---|---|
| **Role** | Regional Director, Legal Metrology Department |
| **Age** | 45-55 |
| **Tech Comfort** | Moderate-High |
| **Work Environment** | Office, regional headquarters |
| **Key Tasks** | Monitor inspection activities, review violation trends, generate compliance statistics |
| **Pain Points** | No centralized data, manual report aggregation, no real-time visibility |
| **Goals** | Dashboard for oversight, exportable reports, search past inspections |

### 3.3 Tertiary Persona: System Administrator

| Attribute | Detail |
|---|---|
| **Role** | IT Support / Department tech lead |
| **Key Tasks** | Deploy system, manage updates, troubleshoot issues |
| **Goals** | Simple deployment, minimal maintenance, Docker support |

---

## 4. Functional Requirements

### FR-01: Image Upload and Product Scanning

| ID | Requirement | Priority |
|---|---|---|
| FR-01.1 | The system SHALL accept image uploads in JPEG, PNG, and WebP formats | P0 |
| FR-01.2 | The system SHALL provide a drag-and-drop upload interface | P0 |
| FR-01.3 | The system SHALL display a preview of the uploaded image before scanning | P0 |
| FR-01.4 | The system SHALL validate file type before processing | P0 |
| FR-01.5 | The system SHALL assign a unique Scan ID to each upload | P0 |
| FR-01.6 | The system SHALL store original uploaded images for evidence | P0 |

### FR-02: Image Preprocessing

| ID | Requirement | Priority |
|---|---|---|
| FR-02.1 | The system SHALL convert uploaded images to grayscale for OCR optimization | P0 |
| FR-02.2 | The system SHALL apply noise reduction (bilateral filtering) while preserving edge sharpness | P0 |
| FR-02.3 | The system SHALL apply adaptive thresholding to handle uneven lighting on curved packaging | P0 |
| FR-02.4 | The system SHALL handle images of varying resolutions and orientations | P1 |

### FR-03: Text Extraction (OCR)

| ID | Requirement | Priority |
|---|---|---|
| FR-03.1 | The system SHALL extract text from packaging labels using OCR | P0 |
| FR-03.2 | The system SHALL support English and Hindi text recognition | P0 |
| FR-03.3 | The system SHALL return bounding box coordinates for each detected text block | P0 |
| FR-03.4 | The system SHALL return confidence scores for each text detection | P0 |
| FR-03.5 | The system SHALL handle multiple text blocks per image | P0 |

### FR-04: Mandatory Declaration Detection

| ID | Requirement | Priority |
|---|---|---|
| FR-04.1 | The system SHALL check for presence of manufacturer/packer/importer name and address (Rule 6(1)(a)) | P0 |
| FR-04.2 | The system SHALL check for net quantity declaration in standard units (Rule 6(1)(b)) | P0 |
| FR-04.3 | The system SHALL check for MRP declaration inclusive of all taxes (Rule 6(1)(c)) | P0 |
| FR-04.4 | The system SHALL check for manufacturing/packing/import date (Rule 6(1)(d)) | P0 |
| FR-04.5 | The system SHALL check for consumer care contact details (Rule 6(1)(e)) | P0 |
| FR-04.6 | The system SHALL check for generic/common name of the commodity (Rule 6(1)(f)) | P0 |
| FR-04.7 | The system SHALL use regex pattern matching for flexible detection of declaration variants | P0 |

### FR-05: Font Size and Readability Analysis

| ID | Requirement | Priority |
|---|---|---|
| FR-05.1 | The system SHALL calculate physical font sizes in millimeters from bounding box dimensions and image DPI | P0 |
| FR-05.2 | The system SHALL check font sizes against minimum thresholds defined in the Rules | P0 |
| FR-05.3 | The system SHALL extract DPI metadata from images when available, with a configurable fallback default | P0 |
| FR-05.4 | The system SHALL flag text blocks that fall below minimum font size requirements | P0 |

### FR-06: Compliance Evaluation

| ID | Requirement | Priority |
|---|---|---|
| FR-06.1 | The system SHALL evaluate each of the 6 mandatory rules as PASS or FAIL | P0 |
| FR-06.2 | The system SHALL determine overall compliance status (COMPLIANT / NON-COMPLIANT) | P0 |
| FR-06.3 | The system SHALL generate a detailed violation list with rule references and descriptions | P0 |
| FR-06.4 | The system SHALL assign severity levels (HIGH/MEDIUM) to violations | P1 |
| FR-06.5 | Overall status SHALL be COMPLIANT only when all rules pass AND no font violations exist | P0 |

### FR-07: PDF Report Generation

| ID | Requirement | Priority |
|---|---|---|
| FR-07.1 | The system SHALL generate a PDF compliance report for each scan | P0 |
| FR-07.2 | The PDF SHALL include scan metadata (ID, date/time, status) | P0 |
| FR-07.3 | The PDF SHALL include a rule-wise compliance results table | P0 |
| FR-07.4 | The PDF SHALL include a detailed violations section | P0 |
| FR-07.5 | The PDF SHALL embed the original product photograph as evidence | P0 |
| FR-07.6 | The PDF SHALL use professional formatting suitable for official/court use | P1 |
| FR-07.7 | The PDF SHALL be downloadable from the web interface | P0 |

### FR-08: CSV Report Generation

| ID | Requirement | Priority |
|---|---|---|
| FR-08.1 | The system SHALL export all compliance records as a downloadable CSV file | P0 |
| FR-08.2 | The CSV SHALL include all scan fields: ID, timestamp, filename, status, rule counts, violations | P0 |
| FR-08.3 | The CSV SHALL be in a standard, editable format compatible with Excel/LibreOffice | P0 |

### FR-09: Scan Repository and History

| ID | Requirement | Priority |
|---|---|---|
| FR-09.1 | The system SHALL store all scan records in a persistent database | P0 |
| FR-09.2 | The system SHALL provide an API endpoint to retrieve all past scan records | P0 |
| FR-09.3 | Records SHALL be stored with scan ID, timestamp, filename, status, rule counts, violations, and extracted text | P0 |
| FR-09.4 | Records SHALL be retrievable in reverse chronological order | P0 |

### FR-10: Dashboard and Analytics

| ID | Requirement | Priority |
|---|---|---|
| FR-10.1 | The system SHALL provide a dashboard showing total scans, compliant count, and non-compliant count | P0 |
| FR-10.2 | The dashboard SHALL display a table of all scan records | P0 |
| FR-10.3 | The dashboard SHALL support client-side search/filter by scan ID, filename, and status | P0 |
| FR-10.4 | The dashboard SHALL provide a one-click CSV export button | P0 |
| FR-10.5 | The dashboard SHALL auto-refresh data on page load | P0 |

### FR-11: Evidence Management

| ID | Requirement | Priority |
|---|---|---|
| FR-11.1 | The system SHALL store original uploaded images as evidence | P0 |
| FR-11.2 | The system SHALL generate annotated evidence images with bounding box overlays | P1 |
| FR-11.3 | Evidence images SHALL be accessible via URL from the scan results | P0 |
| FR-11.4 | Evidence SHALL be embedded in PDF reports | P0 |

### FR-12: User Interface

| ID | Requirement | Priority |
|---|---|---|
| FR-12.1 | The system SHALL provide a web-based Scanner UI for image upload and compliance audit | P0 |
| FR-12.2 | The system SHALL provide a web-based Dashboard UI for analytics and record management | P0 |
| FR-12.3 | Both UIs SHALL work 100% offline with no CDN or external dependencies | P0 |
| FR-12.4 | The UI SHALL be responsive and mobile-friendly | P1 |
| FR-12.5 | The UI SHALL use a dark theme with clear status color coding (green=pass, red=fail) | P1 |

### FR-13: Deployment

| ID | Requirement | Priority |
|---|---|---|
| FR-13.1 | The system SHALL be deployable via Docker with a single command | P0 |
| FR-13.2 | The system SHALL be deployable locally without Docker using Python virtual environment | P0 |
| FR-13.3 | The system SHALL include setup scripts for Windows, Mac, and Linux | P1 |
| FR-13.4 | The system SHALL include a project initialization script for directory scaffolding | P1 |

---

## 5. Non-Functional Requirements

### NFR-01: Performance

| ID | Requirement | Target |
|---|---|---|
| NFR-01.1 | End-to-end scan processing time | ≤ 30 seconds per image |
| NFR-01.2 | OCR model load time (first scan only) | ≤ 15 seconds |
| NFR-01.3 | Subsequent scan processing | ≤ 10 seconds |
| NFR-01.4 | Dashboard page load time | ≤ 2 seconds |
| NFR-01.5 | PDF generation time | ≤ 3 seconds |
| NFR-01.6 | Maximum concurrent users (local deployment) | ≥ 5 |

### NFR-02: Security

| ID | Requirement | Target |
|---|---|---|
| NFR-02.1 | File upload validation | Strict MIME type checking |
| NFR-02.2 | Input sanitization | All file paths use `os.path.join()` |
| NFR-02.3 | Error handling | No stack traces exposed in API responses |
| NFR-02.4 | Data storage | Local-only, no data leaves the deployment |

### NFR-03: Usability

| ID | Requirement | Target |
|---|---|---|
| NFR-03.1 | Time to first scan (new user) | ≤ 60 seconds |
| NFR-03.2 | UI complexity | No training required for basic scanning |
| NFR-03.3 | Visual feedback | Loading spinners, color-coded results |
| NFR-03.4 | Error messaging | User-friendly error messages for all failure modes |

### NFR-04: Reliability

| ID | Requirement | Target |
|---|---|---|
| NFR-04.1 | OCR accuracy on clear images | ≥ 80% rule detection |
| NFR-04.2 | OCR accuracy on noisy/curved images | ≥ 60% rule detection |
| NFR-04.3 | System uptime | 99% (local deployment) |
| NFR-04.4 | Data persistence | SQLite — zero-config, crash-resistant |

### NFR-05: Portability

| ID | Requirement | Target |
|---|---|---|
| NFR-05.1 | Operating systems | Windows 10+, Ubuntu 20.04+, macOS 12+ |
| NFR-05.2 | Python version | 3.10+ |
| NFR-05.3 | GPU requirement | Optional (CPU-only mode fully supported) |
| NFR-05.4 | Internet requirement | **None** — 100% offline operation |
| NFR-05.5 | Container support | Docker + Docker Compose |

---

## 6. System Architecture

### 6.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                             │
│  ┌──────────────┐    ┌────────────────┐                            │
│  │  Scanner UI   │    │  Dashboard UI   │                           │
│  │  index.html   │    │  dashboard.html │                           │
│  │  scanner.js   │    │  dashboard.js   │                           │
│  └───────┬──────┘    └───────┬────────┘                            │
│          │ POST /api/scan     │ GET /api/repository                  │
└──────────┼───────────────────┼──────────────────────────────────────┘
           │                   │
┌──────────┼───────────────────┼──────────────────────────────────────┐
│          ▼                   ▼          SERVER (FastAPI)             │
│  ┌────────────────────────────────────┐                             │
│  │          API Router (routes.py)    │                              │
│  │  /api/scan  /api/repository  /api/export-csv                     │
│  └──────────┬─────────────────────────┘                             │
│             │                                                        │
│  ┌──────────┼──────────────────────────────────────────────┐        │
│  │          ▼         PROCESSING PIPELINE                   │        │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐ │        │
│  │  │ Preprocessor  │→│  OCR Engine  │→│  Font Analyzer  │ │        │
│  │  │  (OpenCV)     │  │  (EasyOCR)   │  │  (DPI→mm)      │ │        │
│  │  └──────────────┘  └──────────────┘  └────────────────┘ │        │
│  │                          │                    │          │        │
│  │                    ┌─────┴────────────────────┘          │        │
│  │                    ▼                                     │        │
│  │  ┌──────────────────────────────────────┐               │        │
│  │  │  Rule Evaluator + Legal Clauses       │               │        │
│  │  │  (6 rules × regex pattern matching)   │               │        │
│  │  └──────────────┬───────────────────────┘               │        │
│  └─────────────────┼───────────────────────────────────────┘        │
│                    │                                                 │
│     ┌──────────────┼─────────────────────┐                          │
│     ▼              ▼                     ▼                          │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐                     │
│  │ PDF Gen  │  │ CSV Gen  │  │ SQLite DB     │                      │
│  │(ReportLab)│  │ (csv)    │  │ (database.py) │                     │
│  └──────────┘  └──────────┘  └───────────────┘                     │
│                                                                      │
│  ┌──────────────────────────────────────────────┐                   │
│  │          STORAGE (storage/)                   │                   │
│  │  uploads/ │ evidence/ │ generated_reports/    │                   │
│  └──────────────────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────┘
```

### 6.2 Technology Justification

| Technology | Chosen | Rationale |
|---|---|---|
| **FastAPI** | Backend framework | Async, auto-docs (Swagger), file upload support, lightweight |
| **EasyOCR** | OCR engine | Multi-language (English+Hindi), no external API, GPU-optional, good accuracy |
| **OpenCV** | Image processing | Industry-standard, bilateral filter + adaptive threshold for packaging images |
| **ReportLab** | PDF generation | Pure Python, no external tools, professional layouts, image embedding |
| **SQLite** | Database | Zero-config, portable, no server needed, perfect for offline deployment |
| **Vanilla JS/CSS** | Frontend | 100% offline, no build tools, no node_modules, zero CDN dependencies |
| **Docker** | Deployment | Reproducible environments, single-command deployment, dependency isolation |

---

## 7. API Specifications

### 7.1 POST `/api/scan`

**Purpose:** Upload a packaged commodity image and receive a full compliance audit.

**Request:**
```
Content-Type: multipart/form-data
Body: file (binary image — JPEG, PNG, or WebP)
```

**Response (200 OK):**
```json
{
    "scan_id": "a1b2c3d4",
    "timestamp": "2025-01-15 14:30:00",
    "filename": "colgate_toothpaste.jpg",
    "compliance_report": {
        "overall_status": "NON-COMPLIANT",
        "total_rules_checked": 6,
        "rules_passed": 4,
        "rules_failed": 2,
        "rule_results": [
            {
                "rule_id": "R1",
                "rule_name": "Name and Address of Manufacturer/Packer/Importer",
                "section": "Rule 6(1)(a)",
                "is_present": true,
                "status": "PASS",
                "matched_patterns_count": 2,
                "matched_snippets": ["manufacturer", "address"],
                "severity": "HIGH"
            }
        ],
        "violations": [
            {
                "rule_id": "R5",
                "rule_name": "Consumer Care Details",
                "section": "Rule 6(1)(e)",
                "severity": "MEDIUM",
                "issue": "Declaration not found: Consumer Care Details"
            }
        ],
        "font_violations": [
            {
                "text": "Net Wt 100g",
                "font_size_mm": 0.8,
                "required_mm": 1.0,
                "issue": "Font size 0.8mm is below minimum 1.0mm"
            }
        ],
        "extracted_text": "Colgate Toothpaste Manufacturer...",
        "total_text_blocks": 15,
        "font_analysis_summary": {
            "total_analyzed": 15,
            "compliant": 13,
            "non_compliant": 2
        }
    },
    "pdf_report": "/storage/generated_reports/a1b2c3d4_report.pdf",
    "evidence_image": "/storage/evidence/a1b2c3d4_evidence.jpg"
}
```

**Error Responses:**
- `400`: Invalid file type
- `500`: Processing failure

### 7.2 GET `/api/repository`

**Purpose:** Retrieve all past scan records.

**Response (200 OK):**
```json
{
    "total": 42,
    "records": [
        {
            "id": 1,
            "scan_id": "a1b2c3d4",
            "timestamp": "2025-01-15 14:30:00",
            "filename": "colgate_toothpaste.jpg",
            "overall_status": "NON-COMPLIANT",
            "total_rules_checked": 6,
            "rules_passed": 4,
            "rules_failed": 2,
            "violations": "[{\"rule_id\": \"R5\", ...}]",
            "extracted_text": "...",
            "created_at": "2025-01-15 14:30:00"
        }
    ]
}
```

### 7.3 GET `/api/export-csv`

**Purpose:** Download all compliance records as a CSV file.

**Response:** `Content-Type: text/csv` file download.

---

## 8. UI Specifications

### 8.1 Scanner Page (`index.html`)

**Layout Sections:**

| Section | Components | Behavior |
|---|---|---|
| **Navbar** | Brand logo, Scanner link (active), Dashboard link | Persistent navigation |
| **Upload Zone** | Dashed border area, drag-and-drop, browse button | Click or drag to select file |
| **Image Preview** | Thumbnail of selected image, "Scan" button | Appears after file selection |
| **Loading State** | Animated spinner, status text | Shown during API call |
| **Results — Status** | Badge showing COMPLIANT (green) or NON-COMPLIANT (red) | Color-coded verdict |
| **Results — Stats** | 3-card grid: Rules Checked, Passed (green), Failed (red) | Numeric counters |
| **Results — Table** | Rule name, Section reference, PASS/FAIL status | Color-coded per row |
| **Results — Violations** | Red-bordered cards listing each violation | Detailed descriptions |
| **Results — Downloads** | PDF report link, Evidence image link | Opens in new tab |

### 8.2 Dashboard Page (`dashboard.html`)

**Layout Sections:**

| Section | Components | Behavior |
|---|---|---|
| **Navbar** | Brand logo, Scanner link, Dashboard link (active) | Persistent navigation |
| **Stats Cards** | Total Scans, Compliant (green), Non-Compliant (red) | Auto-calculated from data |
| **Search Bar** | Text input + Export CSV button | Real-time client-side filtering |
| **Records Table** | Scan ID, Date, Filename, Status, Passed, Failed | Fetched from /api/repository |

### 8.3 Design System

| Element | Value |
|---|---|
| **Background** | #0f0f23 (deep navy) |
| **Surface** | #1a1a2e (card backgrounds) |
| **Border** | #16213e |
| **Primary Text** | #e0e0e0 |
| **Accent** | #00d4ff (cyan) |
| **Success** | #00e676 (green) |
| **Error** | #ff5252 (red) |
| **Secondary Text** | #888888 |
| **Font Stack** | Segoe UI, Tahoma, Geneva, Verdana, sans-serif |
| **Border Radius** | 8-12px |
| **Responsive Breakpoint** | 600px |

---

## 9. Legal Compliance Matrix

**Mapping of Legal Metrology (Packaged Commodities) Rules, 2011 to system features:**

| Rule Section | Legal Requirement | System Feature | Detection Method | Rule ID |
|---|---|---|---|---|
| Rule 6(1)(a) | Manufacturer/Packer/Importer name and address | Mandatory declaration check | Regex: "manufacturer", "packer", "importer", "mfg by", pincode patterns | R1 |
| Rule 6(1)(b) | Net quantity in standard units | Mandatory declaration check | Regex: "net wt/weight/qty" + numeric value + unit (g/kg/ml/L/pcs) | R2 |
| Rule 6(1)(c) | MRP inclusive of all taxes | Mandatory declaration check | Regex: "MRP/M.R.P." + ₹/Rs + amount + "inclusive of all taxes" | R3 |
| Rule 6(1)(d) | Month and year of manufacture/packing/import | Mandatory declaration check | Regex: "mfg date", "best before", "expiry" + date patterns | R4 |
| Rule 6(1)(e) | Consumer care details | Mandatory declaration check | Regex: "consumer care", "helpline", 1800 numbers, email patterns | R5 |
| Rule 6(1)(f) | Common/generic name of commodity | Mandatory declaration check | Regex: "product", "commodity", "ingredients", "contents" | R6 |
| Rule 6(2) | Minimum font size for declarations | Font size analysis | BBox height (px) / DPI × 25.4 = mm, compared against thresholds | Font Check |
| Rule 18 | MRP to include "inclusive of all taxes" | Part of R3 check | Regex specifically for "inclusive of all taxes" clause | R3 |

---

## 10. Database Schema

### `scan_records` Table

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Auto-generated row ID |
| `scan_id` | TEXT | UNIQUE, NOT NULL | 8-character UUID identifier |
| `timestamp` | TEXT | NOT NULL | Scan date and time (YYYY-MM-DD HH:MM:SS) |
| `filename` | TEXT | NOT NULL | Original uploaded filename |
| `overall_status` | TEXT | NOT NULL | COMPLIANT or NON-COMPLIANT |
| `total_rules_checked` | INTEGER | DEFAULT 0 | Number of rules evaluated (always 6) |
| `rules_passed` | INTEGER | DEFAULT 0 | Count of passed rules |
| `rules_failed` | INTEGER | DEFAULT 0 | Count of failed rules |
| `violations` | TEXT | NULLABLE | JSON-serialized array of violation objects |
| `extracted_text` | TEXT | NULLABLE | Full concatenated OCR text |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

---

## 11. Acceptance Criteria

### AC-01: Image Upload
- ✅ User can upload JPEG, PNG, and WebP images via drag-and-drop or file browser
- ✅ Invalid file types are rejected with a clear error message
- ✅ Uploaded image is previewed before scanning

### AC-02: Compliance Scanning
- ✅ System completes a full scan within 30 seconds
- ✅ All 6 mandatory rules are checked for every scan
- ✅ Font sizes are analyzed for all detected text blocks
- ✅ Overall status is correctly determined based on all checks

### AC-03: Report Generation
- ✅ PDF report is generated with scan info, rule results, violations, and embedded photo
- ✅ PDF is downloadable from the results page
- ✅ CSV export includes all scan records with proper formatting

### AC-04: Dashboard
- ✅ Dashboard displays total scans, compliant count, and non-compliant count
- ✅ Search filters records by scan ID, filename, or status in real-time
- ✅ Export CSV button downloads the full compliance history

### AC-05: Offline Operation
- ✅ System functions without any internet connection
- ✅ No external API calls, CDN resources, or cloud dependencies
- ✅ All static assets are served locally

### AC-06: Deployment
- ✅ Docker deployment works with `docker-compose up --build`
- ✅ Local setup works with virtual environment + pip install

---

## 12. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| **Low OCR accuracy on poor-quality images** | High | Medium | Multi-stage preprocessing (grayscale → bilateral filter → adaptive threshold); provide guidelines for photo quality |
| **Font size measurement inaccuracy** | Medium | High | DPI extraction from metadata + configurable default; calibration against known samples |
| **EasyOCR model size (~200MB)** | Low | Medium | Pre-download during setup; Docker layer caching for fast rebuilds |
| **Hindi text recognition quality** | Medium | Medium | EasyOCR supports Hindi; test with diverse Hindi label samples |
| **SQLite concurrency limitations** | Low | Low | Adequate for single-instance deployment; use connection-per-request pattern |
| **Regex pattern false positives/negatives** | Medium | Medium | Extensive pattern testing against ground truth dataset; iterative refinement |
| **Large image processing memory** | Low | Medium | OpenCV headless keeps memory footprint low; monitor with test images |

---

## 13. Success Metrics (KPIs)

| Metric | Target | Measurement |
|---|---|---|
| **Scan Processing Time** | ≤ 30 seconds | Average time from upload to results display |
| **Rule Detection Accuracy** | ≥ 80% on clean images | Comparison against ground truth annotations |
| **Font Size Calculation Accuracy** | ≤ 0.5mm deviation | Comparison against manual ruler measurements |
| **User Task Completion** | ≥ 95% | User successfully completes scan and downloads report |
| **System Uptime** | ≥ 99% | Server availability monitoring |
| **Report Generation Success** | 100% | Every completed scan produces a downloadable PDF |

---

## 14. Release Plan

### Phase 1: MVP (Hackathon Submission) ✅

| Feature | Status |
|---|---|
| Image upload and preview | To implement |
| OCR text extraction (English + Hindi) | To implement |
| 6-rule compliance checking | To implement |
| Font size analysis | To implement |
| PDF report generation with photo evidence | To implement |
| CSV export | To implement |
| Scanner UI | To implement |
| Dashboard with search | To implement |
| SQLite repository | To implement |
| Docker deployment | To implement |

### Phase 2: Post-Hackathon Enhancements

| Feature | Priority |
|---|---|
| Role-based authentication (JWT) | P1 |
| Barcode/QR code scanning | P1 |
| Annotated evidence images with bounding box overlays | P1 |
| Batch image scanning | P2 |
| Additional Indian language OCR support | P2 |
| Mobile application (React Native/Flutter) | P2 |
| Cloud deployment (AWS/GCP) | P2 |
| ML-based label region detection (YOLO) | P3 |
| E-commerce listing scraping | P3 |
| Digital signatures for audit trail | P3 |
| Geographic compliance heatmaps | P3 |

---

## 15. Glossary

| Term | Definition |
|---|---|
| **Legal Metrology** | The science of measurement as applied by law for trade and consumer protection |
| **Packaged Commodity** | Any pre-packaged commodity sealed before sale to consumers |
| **MRP** | Maximum Retail Price — the highest price a retailer can charge, inclusive of all taxes |
| **Net Quantity** | The actual quantity of product in the package, excluding packaging weight |
| **DPI** | Dots Per Inch — image resolution, used to convert pixel measurements to physical mm |
| **OCR** | Optical Character Recognition — technology to extract text from images |
| **Bounding Box** | A rectangular boundary around detected text in an image, defined by 4 corner coordinates |
| **EasyOCR** | Open-source Python OCR library supporting 80+ languages |
| **FastAPI** | Modern Python web framework for building APIs with automatic documentation |
| **ReportLab** | Python library for generating PDF documents programmatically |
| **Adaptive Threshold** | Image processing technique that handles varying lighting conditions across an image |
| **Bilateral Filter** | Image filter that reduces noise while preserving sharp edges |

---

## Appendix A: File Structure

```
nirikshan-core/
├── ARCHITECTURE.md
├── README.md
├── .gitignore
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── database.py
│       ├── vision/
│       │   ├── __init__.py
│       │   ├── preprocessor.py
│       │   ├── ocr_engine.py
│       │   └── font_analyzer.py
│       ├── rules/
│       │   ├── __init__.py
│       │   ├── legal_clauses.py
│       │   └── rule_evaluator.py
│       └── reports/
│           ├── __init__.py
│           ├── pdf_builder.py
│           └── csv_builder.py
├── web/
│   ├── templates/
│   │   ├── index.html
│   │   └── dashboard.html
│   └── static/
│       ├── css/
│       │   └── styles.css
│       └── js/
│           ├── scanner.js
│           └── dashboard.js
├── datasets/
│   ├── raw_samples/
│   └── ground_truth.csv
├── storage/ (gitignored, runtime)
│   ├── uploads/
│   ├── evidence/
│   └── generated_reports/
├── scripts/
│   ├── init_project.py
│   ├── setup_env.bat
│   └── setup_env.sh
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

---

*Document prepared for hackathon submission — Legal Metrology compliance automation using computer vision and rule-based evaluation.*
