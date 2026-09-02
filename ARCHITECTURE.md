# 🏗️ NIRIKSHAN — System Architecture & Design Specification

> **Nirikshan (निरीक्षण)** is an offline-capable, AI-driven compliance auditor for packaged commodities governed by India's **Legal Metrology (Packaged Commodities) Rules, 2011**.

---

## 1. 📌 Project Identity

| Field | Value |
|---|---|
| **Project Name** | Nirikshan — Packaged Commodity Compliance Auditor |
| **Version** | 1.0.0 |
| **Domain** | Legal Metrology Enforcement (India) |
| **Governing Statute** | Legal Metrology Act, 2009 & Legal Metrology (Packaged Commodities) Rules, 2011 |
| **Core Capabilities** | Offline OCR, 6-clause statutory rule evaluation, physical font-size verification, court-ready PDF generation, historical repository |
| **Tech Stack** | Python 3.10+, FastAPI, OpenCV, EasyOCR, ReportLab, SQLite, Vanilla HTML/CSS/JavaScript |
| **Deployment Model** | Single Docker container or local Python virtual environment; 100% offline (air-gapped) |
| **Target Users** | Legal Metrology Inspectors, Enforcement Officers, Regional Directors, Compliance Auditors |

---

## 2. 🗺️ Module Dependency Map

The diagram below illustrates the end-to-end data flow, module interactions, and processing pipeline:

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT LAYER (WEB UI)                             |
|                                                                                   |
|   +------------------------------------+    +---------------------------------+   |
|   | index.html (Scanner Interface)    |    | dashboard.html (Repository View)|   |
|   | scanner.js (Drag/Drop, Upload, UI) |    | dashboard.js (Search, CSV Export|   |
|   +-----------------+------------------+    +----------------+----------------+   |
+---------------------|----------------------------------------|--------------------+
                      | [POST /api/scan (Multipart Image)]     | [GET /api/repository,
                      v                                        |  GET /api/export-csv]
+--------------------------------------------------------------v--------------------+
|                               FASTAPI APPLICATION LAYER                           |
|                                                                                   |
|   backend/app/main.py (Server Bootstrap, Static File & Storage Mounts)           |
|                                       │                                           |
|   backend/app/api/routes.py (REST API Endpoints & Request Orchestration)          |
|                                       │                                           |
|   backend/app/core/config.py (Paths, Legal Thresholds, DPI, Model Constants)      |
+---------------------------------------+-------------------------------------------+
                                        │
           ┌────────────────────────────┴────────────────────────────┐
           ▼                                                         ▼
+───────────────────────────────+                         +─────────────────────────+
|         VISION LAYER          |                         |       RULES LAYER       |
|                               |                         |                         |
| +---------------------------+ |                         | +---------------------+ |
| | preprocessor.py           | |                         | | legal_clauses.py    | |
| | - Grayscale conversion    | |                         | | - 6 Statutory Rules | |
| | - Bilateral filtering     | |                         | | - Case-Insensitive  | |
| | - Adaptive thresholding   | |                         | |   Regex Matchers    | |
| +-------------+-------------+ |                         | +----------+----------+ |
|               │               |                         |            │            |
|               v               |                         |            │            |
| +---------------------------+ |                         |            │            |
| | ocr_engine.py             | |                         |            │            |
| | - EasyOCR Reader Singleton| |                         |            │            |
| | - Bounding Boxes & Text   | |                         |            │            |
| +-------------+-------------+ |                         |            │            |
|               │               |                         |            │            |
|               v               |                         |            │            |
| +---------------------------+ |                         |            v            |
| | font_analyzer.py          | |                         | +---------------------+ |
| | - EXIF / Fallback DPI     | |                         | | rule_evaluator.py   | |
| | - mm = (px / DPI) * 25.4  | ┼────────────────────────►| | - Rule Verification | |
| | - Font compliance check   | |   [OCR BBoxes & Texts]  | | - Font Verification | |
| +---------------------------+ |                         | | - Overall Verdict   | |
+-------------------------------+                         | +----------+----------+ |
                                                          +------------│------------+
                                                                       │
                                        ┌──────────────────────────────┴────────────┐
                                        ▼                                           ▼
+───────────────────────────────────────────────────────────────+ +─────────────────┴───────+
|                         REPORTS LAYER                         | |    PERSISTENCE LAYER    |
|                                                               | |                         |
| +---------------------------+   +---------------------------+ | | +---------------------+ |
| | pdf_builder.py            |   | csv_builder.py            | | | | database.py         | |
| | - ReportLab A4 Document   |   | - UTF-8 Formatted CSV     | | | | - SQLite Connection | |
| | - Legal Inspection Notice |   | - Tabular Audit Records   | | | | - Schema Migration  | |
| | - Embedded Evidence Photo |   | - Download Endpoint Stream| | | | - Save / Query Logs | |
| +---------------------------+   +---------------------------+ | | +---------------------+ |
+---------------------------------------------------------------+ +-------------------------+
                                        │                                           │
                                        ▼                                           ▼
+───────────────────────────────────────────────────────────────────────────────────────────+
|                                RUNTIME STORAGE (storage/)                                 |
|                                                                                           |
|   storage/uploads/        storage/evidence/       storage/generated_reports/   nirikshan.db|
|   (Raw images)            (Annotated previews)    (PDF notices, CSV exports)  (SQLite file|
+───────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 3. 📁 Complete File Registry

The project contains 24 distinct files structured across modular tiers:

| # | File Path | Layer / Module | Purpose & Scope |
|---|---|---|---|
| 1 | `ARCHITECTURE.md` | Documentation | Complete system architecture, dependencies, module breakdown, testing, and team roles |
| 2 | `README.md` | Documentation | Project overview, tech stack, installation, docker instructions, API spec, and hackathon pitch |
| 3 | `PRD.md` | Product Specs | Formal Product Requirements Document detailing user personas, functional & non-functional requirements |
| 4 | `brain.md` | Architecture Source | Comprehensive single-source-of-truth developer guide for implementation and maintenance |
| 5 | `.gitignore` | Configuration | Excludes virtualenvs, cache files, IDE metadata, and runtime storage directories from version control |
| 6 | `backend/requirements.txt` | Dependencies | Locked production dependencies (FastAPI, EasyOCR, OpenCV Headless, ReportLab, Jinja2, etc.) |
| 7 | `backend/app/__init__.py` | Backend Package | Root application package initializer |
| 8 | `backend/app/main.py` | Server Bootstrap | FastAPI application entry point, mounts static/storage assets, configures templates, inits DB |
| 9 | `backend/app/api/__init__.py` | API Layer | Package initialization for API routes |
| 10 | `backend/app/api/routes.py` | API Layer | HTTP route controllers (`/api/scan`, `/api/repository`, `/api/export-csv`, UI templates) |
| 11 | `backend/app/core/__init__.py` | Core Layer | Package initialization for application core |
| 12 | `backend/app/core/config.py` | Core Layer | Central configurations (file paths, legal font thresholds, default DPI, image mime types) |
| 13 | `backend/app/core/database.py` | Core Layer | SQLite database connection management, table schemas, insertion, and retrieval queries |
| 14 | `backend/app/vision/__init__.py` | Vision Layer | Package initialization for computer vision modules |
| 15 | `backend/app/vision/preprocessor.py`| Vision Layer | OpenCV image preprocessing (grayscale, bilateral noise filter, adaptive Gaussian thresholding) |
| 16 | `backend/app/vision/ocr_engine.py` | Vision Layer | Singleton EasyOCR reader management and text/bounding box extraction |
| 17 | `backend/app/vision/font_analyzer.py`| Vision Layer | EXIF DPI extraction, pixel-to-millimeter physical font size calculation and verification |
| 18 | `backend/app/rules/__init__.py` | Rules Layer | Package initialization for compliance rules engine |
| 19 | `backend/app/rules/legal_clauses.py`| Rules Layer | Statutory rule definitions and regex patterns for 6 mandatory Legal Metrology clauses |
| 20 | `backend/app/rules/rule_evaluator.py`| Rules Layer | Two-phase compliance engine evaluating presence of mandatory clauses and font height compliance |
| 21 | `backend/app/reports/__init__.py` | Reports Layer | Package initialization for reporting modules |
| 22 | `backend/app/reports/pdf_builder.py`| Reports Layer | ReportLab-powered court-ready PDF violation notice generator with embedded photo evidence |
| 23 | `backend/app/reports/csv_builder.py`| Reports Layer | Tabular CSV generation utility for bulk compliance history export |
| 24 | `web/templates/index.html` | Frontend UI | Field Inspector Scanner UI with drag-and-drop file upload, live scan progress, and instant results |
| 25 | `web/templates/dashboard.html` | Frontend UI | Central Command Dashboard UI with statistics cards, search bar, and historical scan table |
| 26 | `web/static/css/styles.css` | Frontend Assets | 100% offline dark-theme CSS design system with responsive layouts and accessible typography |
| 27 | `web/static/js/scanner.js` | Frontend Assets | Client-side drag-and-drop handler, image previewer, scan API caller, and DOM result renderer |
| 28 | `web/static/js/dashboard.js` | Frontend Assets | Historical record fetcher, search and filter logic, metrics calculator, and CSV export trigger |
| 29 | `scripts/init_project.py` | Tooling & Scripts | Bootstrapping script that generates all required directory trees and `__init__.py` files |
| 30 | `scripts/setup_env.sh` | Tooling & Scripts | Automated Unix/Linux/macOS script to create virtualenv, upgrade pip, and install dependencies |
| 31 | `scripts/setup_env.bat` | Tooling & Scripts | Automated Windows Batch script for environment setup and dependency installation |
| 32 | `docker/Dockerfile` | Containerization | Production multi-stage Docker build recipe with system graphics libraries and FastAPI CMD |
| 33 | `docker/docker-compose.yml` | Containerization | Docker Compose service definition with persistent volume binding for `./storage` |
| 34 | `datasets/ground_truth.csv` | Testing & QA | Curated test benchmark dataset with ground-truth presence flags for accuracy benchmarking |

---

## 4. 👥 Team Role Assignments

| Role | Primary Responsibilities | Key Deliverables & Modules |
|---|---|---|
| **1. Lead Architect & Backend Engineer** | Overall system architecture, FastAPI setup, SQLite persistence, API endpoints, config management | `main.py`, `routes.py`, `config.py`, `database.py`, `Dockerfile`, `docker-compose.yml` |
| **2. Computer Vision & OCR Engineer** | OpenCV preprocessing pipeline, EasyOCR singleton loader, bounding-box geometry, DPI & font size physics | `preprocessor.py`, `ocr_engine.py`, `font_analyzer.py` |
| **3. Legal Metrology & Rules Engineer** | Domain rule formalization, regex pattern engineering for 6 statutory clauses, two-phase rule evaluation engine | `legal_clauses.py`, `rule_evaluator.py`, legal clause benchmarking |
| **4. Frontend & UX Developer** | Offline-first HTML5/CSS3/JavaScript user interface, dark theme design, drag-and-drop scanner, dashboard analytics | `index.html`, `dashboard.html`, `styles.css`, `scanner.js`, `dashboard.js` |
| **5. QA & DevOps Engineer** | Test dataset curation, ground truth annotation, ReportLab PDF report generation, CSV export, unit/integration testing | `pdf_builder.py`, `csv_builder.py`, `ground_truth.csv`, `init_project.py`, `setup_env.sh/.bat` |

---

## 5. 🧪 Testing Strategy

| Level | Component / Module | Test Description | Success Criteria |
|---|---|---|---|
| **Unit** | `preprocessor.py` | Load sample image file; execute preprocessing pipeline | Returns 2D uint8 numpy array with valid dimensions; handles corrupt files with `ValueError` |
| **Unit** | `ocr_engine.py` | Initialize singleton reader and extract text from sample package | Returns list of dicts with bounding box coordinates, text string, and confidence score > 0.0 |
| **Unit** | `font_analyzer.py` | Provide known bounding box pixel height and DPI (e.g., 42px @ 300 DPI) | Accurately calculates font height in mm using `(px / DPI) * 25.4`; evaluates threshold compliance |
| **Unit** | `legal_clauses.py` | Execute regex patterns on positive and negative text samples for all 6 rules | 100% match on known compliant clause patterns; 0% false positives on unrelated strings |
| **Unit** | `rule_evaluator.py` | Execute two-phase evaluation on mock OCR text & font datasets | Returns dictionary with correct `overall_status`, `rules_passed`, `rules_failed`, and `violations` list |
| **Unit** | `pdf_builder.py` | Generate inspection report from mock scan output and sample image | Generates non-empty valid PDF file with summary table, rule breakdown, and embedded image |
| **Unit** | `csv_builder.py` | Export historical database scan records to CSV string | Generates valid UTF-8 CSV with expected column headers and escaped multi-line text |
| **Integration**| `POST /api/scan` | Upload packaging image through HTTP API endpoint | Returns HTTP 200 with structured JSON compliance report, PDF path, and evidence image path in <30s |
| **Integration**| `GET /api/repository` | Perform scans and retrieve scan history | Returns JSON list containing persisted scan entries matching database state |
| **Integration**| `GET /api/export-csv` | Download compliance history CSV file | Returns HTTP 200 with `text/csv` media type and `Content-Disposition` attachment header |
| **Benchmark**  | Accuracy Evaluation | Evaluate pipeline against `datasets/ground_truth.csv` test set | $\ge 80\%$ rule detection accuracy on standard images; $\ge 60\%$ on curved/shadowed packaging |
