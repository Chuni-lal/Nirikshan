# 🧠 NIRIKSHAN — AI Development Brain File

> **Purpose**: This file is the single source of truth for any AI agent building, extending, or debugging the Nirikshan project. It contains the full architecture, every file's specification, implementation details, legal domain knowledge, data flow diagrams, testing strategy, and deployment instructions. Follow this file top-to-bottom to produce a complete, working system.

---

## 📌 PROJECT IDENTITY

| Field | Value |
|---|---|
| **Project Name** | Nirikshan — Packaged Commodity Compliance Auditor |
| **Version** | 1.0.0 |
| **Domain** | Legal Metrology Enforcement (India) |
| **Governing Law** | Legal Metrology Act, 2009 & Legal Metrology (Packaged Commodities) Rules, 2011 |
| **Tech Stack** | Python 3.10+, FastAPI, EasyOCR, OpenCV, ReportLab, SQLite, Vanilla HTML/CSS/JS |
| **Deployment** | Docker-ready, 100% offline-capable, zero external API dependencies |
| **Target Users** | Legal Metrology Enforcement Officers, Field Inspectors |

---

## 🎯 PROBLEM STATEMENT (Verbatim)

Packaged commodities sold across India must bear mandatory declarations under the Legal Metrology (Packaged Commodities) Rules, 2011 — including manufacturer name/address, net quantity, MRP (inclusive of all taxes), manufacturing date, consumer care details, and the generic commodity name. Manual inspection by enforcement officers is slow (~15 min per product), inconsistent, and cannot scale to the volume of products in the market. **Nirikshan automates the entire compliance pipeline — from image scan to violation report — in under 30 seconds.**

---

## 🏗️ SYSTEM ARCHITECTURE

### High-Level Pipeline

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────┐     ┌──────────────────┐
│  User Upload │ ──▶ │  Preprocessor    │ ──▶ │  OCR Engine   │ ──▶ │  Font Analyzer   │
│  (Image)     │     │  (OpenCV)        │     │  (EasyOCR)    │     │  (DPI → mm)      │
└─────────────┘     └──────────────────┘     └───────────────┘     └──────────────────┘
                                                    │                        │
                                                    ▼                        ▼
                                             ┌──────────────────────────────────┐
                                             │  Rule Evaluator                  │
                                             │  (6 Legal Rules + Font Check)    │
                                             │  ← legal_clauses.py             │
                                             └──────────────────────────────────┘
                                                           │
                                            ┌──────────────┼──────────────┐
                                            ▼              ▼              ▼
                                     ┌────────────┐ ┌────────────┐ ┌───────────┐
                                     │ PDF Report │ │ CSV Export │ │  SQLite   │
                                     │ (ReportLab)│ │ (csv)      │ │  Database │
                                     └────────────┘ └────────────┘ └───────────┘
```

### Request Flow (POST /api/scan)

1. User uploads image via `index.html` → `scanner.js` sends `FormData` to `/api/scan`
2. `routes.py` validates file type, generates `scan_id`, saves upload to `storage/uploads/`
3. `preprocessor.py` — grayscale → bilateral filter → adaptive threshold
4. `ocr_engine.py` — EasyOCR extracts text + bounding boxes
5. `font_analyzer.py` — converts bbox pixel heights to physical mm using DPI
6. `rule_evaluator.py` — checks all 6 mandatory rules + font compliance
7. `pdf_builder.py` — generates court-ready PDF with tables + photo evidence
8. `database.py` — persists scan record to SQLite
9. JSON response returned with compliance report, PDF link, evidence link

---

## 📁 COMPLETE FILE REGISTRY & IMPLEMENTATION SPECS

### Root Files

#### `ARCHITECTURE.md`
- Module dependency map, file registry, team roles, testing strategy
- **Already complete** — no changes needed

#### `README.md`
- Project summary, tech stack, quick start, docker deployment, API docs, pitch deck
- **Already complete** — no changes needed

#### `.gitignore`
- Ignores: `venv/`, `__pycache__/`, `storage/`, IDE files, OS files
- **Already complete** — no changes needed

---

### Backend: `backend/`

#### `backend/requirements.txt`
**Locked dependencies (do NOT change versions without testing):**
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
easyocr==1.7.1
opencv-python-headless==4.8.1.78
reportlab==4.0.8
Pillow==10.1.0
jinja2==3.1.2
aiofiles==23.2.1
```

> [!CAUTION]
> `opencv-python-headless` is used instead of `opencv-python` to avoid GUI dependency issues in Docker/server environments. Do NOT switch to `opencv-python`.

---

### Backend App: `backend/app/`

#### `backend/app/__init__.py`
- Empty file — makes `app` a Python package

#### `backend/app/main.py` — Server Bootstrap
**Responsibilities:**
1. Create FastAPI app with title, description, version metadata
2. Ensure all `storage/` subdirectories exist on startup
3. Call `init_db()` to create SQLite tables
4. Mount static files from `web/static/` at `/static`
5. Mount storage directory at `/storage` for serving evidence/reports
6. Set up Jinja2 templates from `web/templates/`
7. Include API router from `routes.py`
8. Serve `index.html` at `/` (Scanner UI)
9. Serve `dashboard.html` at `/dashboard` (Dashboard UI)

**Key implementation details:**
- Static files path: `../../web/static` (relative from `main.py`)
- Templates path: `../../web/templates` (relative from `main.py`)
- Storage mount serves uploaded images, evidence, and generated reports directly

---

### API Layer: `backend/app/api/`

#### `backend/app/api/__init__.py`
- Empty file

#### `backend/app/api/routes.py` — API Endpoints
**Three endpoints:**

| Endpoint | Method | Input | Output | Purpose |
|---|---|---|---|---|
| `/api/scan` | POST | `UploadFile` (image) | JSON compliance report | Full scan pipeline |
| `/api/repository` | GET | None | JSON array of records | Fetch all past scans |
| `/api/export-csv` | GET | None | CSV file download | Export compliance history |

**`POST /api/scan` — Detailed Flow:**
1. Validate `content_type` ∈ `["image/jpeg", "image/png", "image/jpg", "image/webp"]`
2. Generate `scan_id` = first 8 chars of UUID4
3. Save file to `storage/uploads/{scan_id}{ext}`
4. Call pipeline: `preprocess_image()` → `extract_text()` → `analyze_font_sizes()` → `evaluate_compliance()`
5. Generate evidence image at `storage/evidence/{scan_id}_evidence.jpg`
6. Generate PDF at `storage/generated_reports/{scan_id}_report.pdf`
7. Save to database via `save_scan_record()`
8. Return JSON:
```json
{
    "scan_id": "a1b2c3d4",
    "timestamp": "2025-01-01 12:00:00",
    "filename": "product.jpg",
    "compliance_report": { ... },
    "pdf_report": "/storage/generated_reports/a1b2c3d4_report.pdf",
    "evidence_image": "/storage/evidence/a1b2c3d4_evidence.jpg"
}
```

**Error handling:** HTTPException with 400 for invalid file type, 500 for processing failures

---

### Core Layer: `backend/app/core/`

#### `backend/app/core/__init__.py`
- Empty file

#### `backend/app/core/config.py` — Global Configuration
**Constants to define:**

| Constant | Value | Purpose |
|---|---|---|
| `BASE_DIR` | 4 levels up from config.py | Project root |
| `STORAGE_DIR` | `{BASE_DIR}/storage` | Runtime storage root |
| `UPLOADS_DIR` | `{STORAGE_DIR}/uploads` | Raw uploaded images |
| `EVIDENCE_DIR` | `{STORAGE_DIR}/evidence` | Annotated evidence images |
| `REPORTS_DIR` | `{STORAGE_DIR}/generated_reports` | PDF and CSV reports |
| `DATABASE_PATH` | `{STORAGE_DIR}/nirikshan.db` | SQLite database file |
| `OCR_LANGUAGES` | `["en", "hi"]` | English + Hindi OCR |
| `OCR_GPU` | `False` | Set True if CUDA available |
| `DEFAULT_DPI` | `300` | Fallback DPI for font calc |
| `ALLOWED_EXTENSIONS` | `{".jpg", ".jpeg", ".png", ".webp"}` | Valid image formats |

**Font Size Thresholds (Legal Metrology Rules):**
```python
FONT_SIZE_THRESHOLDS = {
    "net_quantity": {
        "area_<=_100_cm2": 1.0,      # Min 1mm for packages ≤ 100 cm²
        "area_100-500_cm2": 2.0,      # Min 2mm for 100-500 cm²
        "area_500-2500_cm2": 4.0,     # Min 4mm for 500-2500 cm²
        "area_>_2500_cm2": 6.0,       # Min 6mm for > 2500 cm²
    },
    "mrp": 2.0,
    "generic_declaration": 1.0,
}
```

#### `backend/app/core/database.py` — SQLite Database
**Schema — `scan_records` table:**

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `scan_id` | TEXT | UNIQUE NOT NULL |
| `timestamp` | TEXT | NOT NULL |
| `filename` | TEXT | NOT NULL |
| `overall_status` | TEXT | NOT NULL (`COMPLIANT` or `NON-COMPLIANT`) |
| `total_rules_checked` | INTEGER | DEFAULT 0 |
| `rules_passed` | INTEGER | DEFAULT 0 |
| `rules_failed` | INTEGER | DEFAULT 0 |
| `violations` | TEXT | JSON string of violation array |
| `extracted_text` | TEXT | Full OCR text |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**Functions:**
- `get_connection()` — returns connection with `row_factory = sqlite3.Row`
- `init_db()` — CREATE TABLE IF NOT EXISTS
- `save_scan_record(scan_id, timestamp, filename, compliance_report)` — extracts fields from report dict, serializes violations as JSON
- `get_all_records()` — SELECT * ORDER BY created_at DESC, returns list of dicts

---

### Vision Layer: `backend/app/vision/`

#### `backend/app/vision/__init__.py`
- Empty file

#### `backend/app/vision/preprocessor.py` — Image Preprocessing
**Pipeline:**
1. `cv2.imread(image_path)` — load image
2. `cv2.cvtColor(image, COLOR_BGR2GRAY)` — grayscale conversion
3. `cv2.bilateralFilter(gray, 9, 75, 75)` — noise reduction preserving edges
4. `cv2.adaptiveThreshold(filtered, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 11, 2)` — handles uneven lighting on curved packaging

**Input:** image file path
**Output:** preprocessed numpy array
**Error:** raises ValueError if image cannot be loaded

> [!IMPORTANT]
> The bilateral filter parameters (d=9, sigmaColor=75, sigmaSpace=75) are tuned for typical packaging photos. The adaptive threshold (blockSize=11, C=2) handles curved surfaces and shadows. Do not change these without testing on the full dataset.

#### `backend/app/vision/ocr_engine.py` — OCR Text Extraction
**Implementation:**
- Singleton pattern for EasyOCR reader (model loads once, reused)
- `get_reader()` — lazy initialization of `easyocr.Reader(["en", "hi"], gpu=False)`
- `extract_text(image_path)` — runs `reader.readtext(image_path, detail=1)`

**Output format (list of dicts):**
```python
[
    {
        "bbox": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],  # 4 corner points
        "text": "MRP ₹150",
        "confidence": 0.9432
    },
    ...
]
```

> [!NOTE]
> EasyOCR's first call takes 5-10 seconds to load the model. Subsequent calls are fast. The singleton pattern ensures this only happens once per server lifecycle.

#### `backend/app/vision/font_analyzer.py` — Font Size Analysis
**Core formula:**
```
font_size_mm = (bbox_height_px / DPI) × 25.4
```

**Functions:**
- `get_image_dpi(image_path)` — extracts DPI from EXIF/image metadata via Pillow, falls back to DEFAULT_DPI (300)
- `calculate_font_size_mm(bbox_height_px, dpi)` — applies the formula
- `get_bbox_height(bbox)` — calculates pixel height from 4-corner bbox (`abs(bottom_left[1] - top_left[1])`)
- `analyze_font_sizes(ocr_results, image_path)` — iterates all OCR results, calculates mm sizes, checks against `FONT_SIZE_THRESHOLDS["generic_declaration"]` (1.0mm minimum)

**Output format (list of dicts):**
```python
[
    {
        "text": "Net Wt 500g",
        "bbox": [[...], [...], [...], [...]],
        "bbox_height_px": 42.5,
        "dpi": 300,
        "font_size_mm": 3.59,
        "min_required_mm": 1.0,
        "is_compliant": True
    },
    ...
]
```

---

### Rules Layer: `backend/app/rules/`

#### `backend/app/rules/__init__.py`
- Empty file

#### `backend/app/rules/legal_clauses.py` — Statutory Rule Definitions

> [!IMPORTANT]
> These 6 rules are derived from the Legal Metrology (Packaged Commodities) Rules, 2011. Every rule has regex patterns for automated detection. These patterns are critical for accuracy — modify with extreme care.

**The 6 Mandatory Rules:**

| Rule ID | Rule Name | Section | Severity | Detection Strategy |
|---|---|---|---|---|
| R1 | Name & Address of Manufacturer/Packer/Importer | Rule 6(1)(a) | HIGH | Match keywords: manufacturer, packer, importer, packed by, made by, mfg by, mfd by + address/pincode patterns |
| R2 | Net Quantity Declaration | Rule 6(1)(b) | HIGH | Match "net wt/weight/qty/quantity/content" + numeric value with unit (g, kg, ml, l, pieces, etc.) |
| R3 | Maximum Retail Price (MRP) | Rule 6(1)(c) | HIGH | Match "MRP" or "maximum retail price" + currency symbol (₹/Rs) + number + "inclusive of all taxes" |
| R4 | Date of Manufacture/Packing/Import | Rule 6(1)(d) | HIGH | Match "mfg date", "mfd", "best before", "expiry", "use by" + date patterns (month names, DD/MM/YYYY) |
| R5 | Consumer Care Details | Rule 6(1)(e) | MEDIUM | Match "consumer care", "customer care", "helpline", "toll free" + 1800 numbers, 10-digit phones, email patterns |
| R6 | Common/Generic Name of Commodity | Rule 6(1)(f) | MEDIUM | Match "product", "commodity", "ingredient", "composition", "content" |

**Each rule object structure:**
```python
{
    "rule_id": "R1",
    "rule_name": "Name and Address of Manufacturer/Packer/Importer",
    "section": "Rule 6(1)(a)",
    "description": "Every package must declare...",
    "patterns": [regex1, regex2, ...],  # List of regex patterns
    "keywords": ["manufacturer", "packer", ...],  # Human-readable keywords
    "severity": "HIGH"  # HIGH or MEDIUM
}
```

**Functions:**
- `get_all_rules()` — returns the `MANDATORY_RULES` list
- `match_rule(rule, text)` — runs all regex patterns against full extracted text, returns match status, count, and up to 5 unique snippets

#### `backend/app/rules/rule_evaluator.py` — Compliance Engine
**Two-phase evaluation:**

**Phase 1 — Rule Presence Check:**
- Concatenates all OCR text into single string
- Runs `match_rule()` for each of the 6 rules
- Each rule gets PASS (pattern matched) or FAIL (not found)

**Phase 2 — Font Size Check:**
- Iterates font analysis results
- Any text block below minimum threshold → font violation

**Output — Compliance Report:**
```python
{
    "overall_status": "COMPLIANT" | "NON-COMPLIANT",
    "total_rules_checked": 6,
    "rules_passed": 4,
    "rules_failed": 2,
    "rule_results": [ ... ],        # Per-rule PASS/FAIL details
    "violations": [ ... ],           # Failed rules with descriptions
    "font_violations": [ ... ],      # Font size violations
    "extracted_text": "full text...",
    "total_text_blocks": 15,
    "font_analysis_summary": {
        "total_analyzed": 15,
        "compliant": 13,
        "non_compliant": 2
    }
}
```

**Decision logic:** `overall_status = "COMPLIANT"` only if `rules_failed == 0 AND font_violations == 0`

---

### Reports Layer: `backend/app/reports/`

#### `backend/app/reports/__init__.py`
- Empty file

#### `backend/app/reports/pdf_builder.py` — PDF Report Generator
**Uses ReportLab to generate A4 PDF with:**
1. **Title**: "NIRIKSHAN — Compliance Inspection Report"
2. **Scan Info Table**: scan_id, timestamp, overall status, rules checked/passed/failed
3. **Rule-wise Results Table**: rule_id, rule_name, section, PASS/FAIL status (color-coded)
4. **Violations List**: detailed violation descriptions (if any)
5. **Photo Evidence**: embedded original upload image (4×3 inches, centered)
6. **Footer**: "Generated by Nirikshan" + legal reference

**Styling:**
- Title: 18pt, color #1a1a2e
- Info table: gray headers, Helvetica, 10pt
- Rules table: dark blue header (#16213e), white text, bold
- Page margins: 20mm top/bottom, 15mm left/right

#### `backend/app/reports/csv_builder.py` — CSV Export Generator
**CSV columns:**
```
Scan ID | Timestamp | Filename | Overall Status | Rules Checked | Rules Passed | Rules Failed | Violations | Extracted Text
```

**Notes:**
- Violations are joined with "; " separator
- Extracted text truncated to 200 characters
- Handles empty records gracefully (writes headers only)
- Uses UTF-8 encoding

---

### Frontend: `web/`

#### `web/templates/index.html` — Scanner UI (Field Inspector)
**Structure:**
1. **Navbar**: Brand "🔍 NIRIKSHAN" + links to Scanner (active) and Dashboard
2. **Upload Area**: Drag-and-drop zone with browse button, file input (hidden)
3. **Preview Section**: Shows uploaded image + "Scan for Compliance" button
4. **Loader**: Spinning animation with "Analyzing packaging label..." text
5. **Results Section**:
   - Status badge (COMPLIANT green / NON-COMPLIANT red)
   - Stats grid: Rules Checked, Passed, Failed
   - Rules table with per-rule status
   - Violations list (red left border cards)
   - Report download links (PDF + Evidence)

#### `web/templates/dashboard.html` — Dashboard UI (Central Command)
**Structure:**
1. **Navbar**: Same as Scanner, Dashboard link active
2. **Dashboard Stats**: Total Scans, Compliant count, Non-Compliant count
3. **Search Bar**: Text filter + Export CSV button
4. **Records Table**: Scan ID, Date, Filename, Status, Passed, Failed

#### `web/static/css/styles.css` — 100% Offline Styling
**Design system:**
- **Background**: Dark theme (#0f0f23)
- **Text**: Light (#e0e0e0)
- **Accent**: Cyan (#00d4ff)
- **Success**: Green (#00e676)
- **Error**: Red (#ff5252)
- **Card background**: #1a1a2e
- **Font**: Segoe UI fallback stack
- **Fully responsive** (mobile-friendly grid)

> [!NOTE]
> No CDN dependencies. No external fonts. No external CSS frameworks. The entire UI works 100% offline, which is critical for field deployment in areas with no internet.

#### `web/static/js/scanner.js` — Scanner Logic
**Functionality:**
1. Drag-and-drop + click-to-browse file handling
2. Client-side image preview (FileReader API)
3. FormData POST to `/api/scan`
4. Dynamic DOM rendering of compliance results
5. Status badge, stats grid, rules table, violations list, report links

#### `web/static/js/dashboard.js` — Dashboard Logic
**Functionality:**
1. Fetch `/api/repository` on page load
2. Render records table dynamically
3. Update stats counters (total, compliant, non-compliant)
4. Client-side search filter (scan_id, filename, status)
5. Export CSV button → `window.location.href = '/api/export-csv'`

---

### Scripts: `scripts/`

#### `scripts/init_project.py`
- Creates all directories and `__init__.py` files
- Run once after cloning

#### `scripts/setup_env.sh` (Linux/Mac)
- Creates venv, activates it, installs requirements

#### `scripts/setup_env.bat` (Windows)
- Same as above for Windows

---

### Docker: `docker/`

#### `docker/Dockerfile`
```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### `docker/docker-compose.yml`
- Single service `nirikshan`
- Maps port 8000, mounts storage volume
- `restart: unless-stopped`

---

### Storage: `storage/` (Runtime, gitignored)

| Directory | Purpose |
|---|---|
| `storage/uploads/` | Raw uploaded packaging photos |
| `storage/evidence/` | Processed images with annotated bounding boxes |
| `storage/generated_reports/` | PDF notices and CSV exports |
| `storage/nirikshan.db` | SQLite database file |

---

### Datasets: `datasets/`

#### `datasets/raw_samples/`
- Should contain 15-20 test packaging images (clean, noisy, curved surfaces, different lighting)
- Cover various product types: FMCG, food, cosmetics, electronics

#### `datasets/ground_truth.csv`
- **Columns**: `filename, manufacturer_present, net_qty_present, mrp_present, mfg_date_present, consumer_care_present, generic_name_present, mrp_value, net_qty_value, expected_overall_status`
- Manual annotations for accuracy benchmarking
- Each row = one test image

---

## ⚖️ LEGAL DOMAIN KNOWLEDGE

### Legal Metrology (Packaged Commodities) Rules, 2011 — Key Provisions

**Rule 6(1)** — Every pre-packaged commodity shall bear the following mandatory declarations:

| Sub-rule | Declaration | Details |
|---|---|---|
| (a) | **Manufacturer/Packer/Importer** | Full name and complete address including pincode |
| (b) | **Net Quantity** | In standard units: weight (g/kg), volume (ml/L), length (cm/m), or number |
| (c) | **MRP** | "Maximum Retail Price" or "MRP" followed by amount inclusive of all taxes |
| (d) | **Manufacturing/Packing Date** | Month and year of manufacture, packing, or import |
| (e) | **Consumer Care** | Name, address, phone/email of consumer care department |
| (f) | **Generic/Common Name** | The common or generic name of the commodity |

**Rule 6(2)** — Font Size Requirements:
- Net quantity font size depends on principal display panel area
- MRP must be prominent and legible (≥ 2mm recommended)
- All declarations must be legible and conspicuous

**Rule 18** — MRP must include "inclusive of all taxes"

**Rule 24** — Declarations must not be misleading

---

## 🧪 TESTING STRATEGY

### Unit Tests
| Module | Test |
|---|---|
| `preprocessor.py` | Load image → verify output is numpy array, verify shape |
| `ocr_engine.py` | Extract text from known image → verify key text found |
| `font_analyzer.py` | Given known bbox height and DPI → verify mm calculation |
| `legal_clauses.py` | Match each rule pattern against known compliant/non-compliant text |
| `rule_evaluator.py` | Full evaluation with mock data → verify PASS/FAIL counts |
| `pdf_builder.py` | Generate PDF → verify file exists and is valid |
| `csv_builder.py` | Generate CSV → verify headers and row count |

### Integration Tests
| Test | Scope |
|---|---|
| Full scan pipeline | Upload image → verify JSON response structure |
| Repository retrieval | Scan → fetch records → verify scan appears |
| CSV export | Scan → export → verify CSV contains record |

### Accuracy Benchmarking
- Compare OCR output against `ground_truth.csv`
- Target: ≥ 80% rule detection accuracy on clean images
- Target: ≥ 60% on noisy/curved images

---

## 🚀 DEPLOYMENT INSTRUCTIONS

### Local Development
```bash
git clone <repo-url>
cd nirikshan-core
python scripts/init_project.py
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
cd docker
docker-compose up --build
```

### Access Points
- Scanner UI: http://localhost:8000
- Dashboard UI: http://localhost:8000/dashboard
- API Docs: http://localhost:8000/docs (FastAPI auto-generated Swagger)

---

## 🔮 FUTURE ENHANCEMENTS (Phase 2)

> [!TIP]
> These are NOT required for the hackathon MVP but demonstrate scalability:

1. **Role-based authentication** — JWT tokens, login/signup, admin vs inspector roles
2. **Barcode/QR code scanning** — Extract product codes for database cross-referencing
3. **Multi-language OCR** — Add Tamil, Telugu, Bengali, Marathi support
4. **Mobile app** — React Native or Flutter wrapper for field use
5. **Cloud deployment** — AWS/GCP with S3 storage and PostgreSQL
6. **Batch scanning** — Upload multiple images for bulk compliance checking
7. **ML-based label region detection** — YOLO/SSD to locate label areas before OCR
8. **E-commerce integration** — Scrape product listings for online compliance checking
9. **Audit trail with digital signatures** — Tamper-proof evidence chain
10. **Real-time analytics** — Violation trends, geographic heatmaps, compliance rates

---

## 📋 IMPLEMENTATION CHECKLIST

Use this checklist to track progress. Every item corresponds to a file in the project:

### Backend Core
- [ ] `backend/app/main.py` — Server bootstrap, route mounting, static serving
- [ ] `backend/app/core/config.py` — All constants, paths, thresholds
- [ ] `backend/app/core/database.py` — SQLite init, save, query

### API
- [ ] `backend/app/api/routes.py` — /api/scan, /api/repository, /api/export-csv

### Vision Pipeline
- [ ] `backend/app/vision/preprocessor.py` — OpenCV preprocessing pipeline
- [ ] `backend/app/vision/ocr_engine.py` — EasyOCR singleton + text extraction
- [ ] `backend/app/vision/font_analyzer.py` — DPI-based mm calculation

### Rules Engine
- [ ] `backend/app/rules/legal_clauses.py` — 6 rules + regex patterns
- [ ] `backend/app/rules/rule_evaluator.py` — Compliance evaluation engine

### Reports
- [ ] `backend/app/reports/pdf_builder.py` — ReportLab PDF generator
- [ ] `backend/app/reports/csv_builder.py` — CSV export generator

### Frontend
- [ ] `web/templates/index.html` — Scanner UI
- [ ] `web/templates/dashboard.html` — Dashboard UI
- [ ] `web/static/css/styles.css` — Dark theme, responsive, offline
- [ ] `web/static/js/scanner.js` — Upload, scan, render results
- [ ] `web/static/js/dashboard.js` — Fetch records, search, export

### Infrastructure
- [ ] `scripts/init_project.py` — Directory scaffolding
- [ ] `scripts/setup_env.sh` — Linux/Mac setup
- [ ] `scripts/setup_env.bat` — Windows setup
- [ ] `docker/Dockerfile` — Container image
- [ ] `docker/docker-compose.yml` — Container orchestration
- [ ] `datasets/ground_truth.csv` — Test benchmarks
- [ ] `datasets/raw_samples/` — 15-20 test images

---

## ⚡ CRITICAL IMPLEMENTATION NOTES

> [!WARNING]
> **These are non-negotiable constraints. Violating any of these will break the system or disqualify the submission:**

1. **100% Offline** — No external API calls. No CDN. No cloud services. Everything runs locally.
2. **EasyOCR Singleton** — The reader MUST be initialized once and reused. Re-initializing per request will cause 5-10 second delays and memory issues.
3. **OpenCV Headless** — Use `opencv-python-headless`, never `opencv-python` in production/Docker.
4. **SQLite Thread Safety** — Create new connections per request, don't share connections across threads.
5. **File Paths** — Always use `os.path.join()`, never hardcode path separators. Must work on Windows AND Linux.
6. **Storage Directory** — Must be created at runtime, must be in `.gitignore`, must not contain any tracked files.
7. **Font Size Calculation** — The formula `(bbox_height_px / DPI) × 25.4` is the correct physics. Do not approximate or skip DPI extraction.
8. **Regex Patterns** — All patterns use `(?i)` flag for case-insensitive matching. This is essential since OCR output casing is unpredictable.
9. **JSON Serialization** — Violations must be stored as JSON strings in SQLite, deserialized on retrieval.
10. **PDF Evidence** — The original uploaded image must be embedded in the PDF, not the preprocessed version.

---

## 🎤 HACKATHON PRESENTATION TALKING POINTS

1. **Problem**: Manual inspection of packaged goods is slow (15 min/product), inconsistent, and doesn't scale
2. **Solution**: Nirikshan automates the entire pipeline — image → OCR → rule check → report — in <30 seconds
3. **Demo Flow**: Upload image → show loading → show PASS/FAIL results → download PDF report → show dashboard
4. **Technical Differentiation**: Physical font size verification (not just OCR), court-ready PDF evidence, 100% offline
5. **Impact**: 30x faster inspections, standardized compliance checking, digital audit trail
6. **Scalability**: Modular architecture, Docker-ready, extensible rule engine for new regulations

---

## 📜 CONVERSATION HISTORY & AGENT MEMORY LOGS

| Session ID | Date | Key Milestones & Enhancements |
|---|---|---|
| [`01c9f0a5-7dd8-496c-bc5e-a76d9d2cabfb`](conversation://01c9f0a5-7dd8-496c-bc5e-a76d9d2cabfb) | 2026-09-04 | Initial OCR upscaling, line reconstruction, and FastAPI setup |
| [`8163ee2f-088d-44aa-8cde-43c7ecb276a3`](conversation://8163ee2f-088d-44aa-8cde-43c7ecb276a3) | 2026-09-04 | DoCA Official UI, NVIDIA CUDA GPU acceleration, Dot-matrix morphological closing, Proximity line clustering, Structured Key-Value summary grid, Windows/Mac 1-click launchers (`run_windows.bat`), and Sandbox repository creation (`Nirikshan-Sandbox.git`) |

