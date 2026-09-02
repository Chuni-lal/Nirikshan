# 🔍 NIRIKSHAN (निरीक्षण)
### Packaged Commodity Legal Metrology Compliance Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![100% Offline](https://img.shields.io/badge/Offline-100%25%20Air--Gapped-green.svg)]()

> **Nirikshan** is an AI-powered compliance auditing platform engineered for Indian **Legal Metrology Enforcement Officers**. It automates label verification for packaged commodities under the **Legal Metrology (Packaged Commodities) Rules, 2011**, transforming a 15-minute manual inspection into an instant, objective, and court-ready audit report in under 30 seconds.

---

## 🎯 Hackathon Pitch & Overview

### 1. The Problem
India's retail landscape spans millions of pre-packaged commodities. Under the **Legal Metrology (Packaged Commodities) Rules, 2011**, all packages must declare 6 mandatory statements:
1. Name & complete address of Manufacturer / Packer / Importer (`Rule 6(1)(a)`)
2. Net Quantity in standard metric units (`Rule 6(1)(b)`)
3. Maximum Retail Price (MRP) inclusive of all taxes (`Rule 6(1)(c)`)
4. Month and Year of Manufacture / Packing / Import (`Rule 6(1)(d)`)
5. Consumer Care contact details (`Rule 6(1)(e)`)
6. Common or Generic Name of the commodity (`Rule 6(1)(f)`)

**Current Pain Points:**
- **Manual & Slow**: Field officers spend 10–15 minutes per product manually measuring fonts and verifying statements.
- **Inconsistent Enforcement**: Subjective human interpretations lead to disputed notices.
- **Low Inspection Coverage**: Millions of SKUs remain unchecked due to workforce constraints.
- **Paper-Based Records**: Lack of centralized audit trails and standard photographic evidence.

### 2. The Nirikshan Solution
Nirikshan automates the complete compliance pipeline:
- **Instant Optical Scan**: Extracts bilingual text (English & Hindi) using EasyOCR with OpenCV adaptive filtering for curved and uneven packaging surfaces.
- **Statutory Rules Engine**: Validates all 6 mandatory declarations via robust legal pattern matchers.
- **Physical Font Height Verification**: Computes real-world font height in millimeters using optical bounding box geometry and EXIF DPI metadata (`(pixels / DPI) × 25.4`).
- **Court-Ready PDF Reports**: Automatically compiles legal violation notices complete with embedded evidence photos and timestamped audit metadata.
- **100% Offline & Private**: Zero external API dependencies, runs fully air-gapped on field laptops or local edge devices.

### 3. Measurable Impact
- ⚡ **30x Faster Inspections**: Reduces audit turnaround from ~15 minutes to < 30 seconds.
- 🎯 **Standardized & Objective**: Eliminates human subjectivity in font size and declaration compliance.
- 📜 **Litigation-Grade Evidence**: Standardized PDF notices ready for legal proceedings under the Legal Metrology Act, 2009.
- 📊 **Centralized Analytics**: Real-time violation tracking, trend analysis, and CSV reporting.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance asynchronous REST API server |
| **OCR Engine** | [EasyOCR](https://github.com/JaidedAI/EasyOCR) | Offline neural OCR supporting English & Hindi text detection |
| **Vision & Image Processing** | [OpenCV](https://opencv.org/) (`opencv-python-headless`) | Bilateral noise filtering, adaptive thresholding, bounding box extraction |
| **Font Physics Engine** | [Pillow (PIL)](https://python-pillow.org/) + Custom Math | EXIF DPI extraction & physical millimeter height computation |
| **Report Generation** | [ReportLab](https://www.reportlab.com/) | Dynamic court-ready PDF generation with embedded photo evidence |
| **Database** | [SQLite3](https://www.sqlite.org/) | Lightweight, serverless local database for audit trail logs |
| **Frontend** | Vanilla HTML5 / CSS3 / ES6 JavaScript | 100% offline responsive dark-theme interface (no CDN dependencies) |
| **Containerization** | [Docker](https://www.docker.com/) & Docker Compose | Self-contained, portable, reproducible deployment |

---

## 📂 Project Structure

```
nirikshan/
├── ARCHITECTURE.md          # Detailed technical architecture specification
├── PRD.md                   # Formal Product Requirements Document
├── README.md                # Project documentation and quick-start guide
├── brain.md                 # Single source of truth developer blueprint
├── .gitignore               # Git ignore rules for venv, storage, and caches
├── backend/
│   ├── requirements.txt     # Python dependency lockfile
│   └── app/
│       ├── __init__.py
│       ├── main.py          # FastAPI application bootstrap & static mounts
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py    # REST API endpoints (/api/scan, /api/repository, etc.)
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py    # System constants, legal thresholds, paths
│       │   └── database.py  # SQLite schema initialization and CRUD operations
│       ├── vision/
│       │   ├── __init__.py
│       │   ├── preprocessor.py # OpenCV grayscale, bilateral & adaptive filters
│       │   ├── ocr_engine.py   # EasyOCR singleton model loader & extractor
│       │   └── font_analyzer.py# Physical font height (mm) calculation
│       ├── rules/
│       │   ├── __init__.py
│       │   ├── legal_clauses.py# Legal Metrology 6-clause statutory regexes
│       │   └── rule_evaluator.py # Two-phase compliance verification engine
│       └── reports/
│           ├── __init__.py
│           ├── pdf_builder.py  # Court-ready PDF inspection notice builder
│           └── csv_builder.py  # Tabular CSV export utility
├── datasets/
│   ├── ground_truth.csv     # Test dataset annotations for benchmark accuracy
│   └── raw_samples/         # Sample packaging test images
├── docker/
│   ├── Dockerfile           # Multi-stage container definition
│   └── docker-compose.yml   # Multi-container orchestration & storage mapping
├── scripts/
│   ├── init_project.py      # Automated project scaffolding script
│   ├── setup_env.sh         # Linux / macOS automated environment setup
│   └── setup_env.bat        # Windows automated environment setup
├── storage/                 # Runtime storage (gitignored)
│   ├── uploads/             # Raw uploaded packaging photos
│   ├── evidence/            # Annotated evidence photos
│   ├── generated_reports/   # Generated PDF & CSV reports
│   └── nirikshan.db         # SQLite database file
└── web/
    ├── templates/
    │   ├── index.html       # Field Inspector Scanner UI
    │   └── dashboard.html   # Central Command Repository Dashboard UI
    └── static/
        ├── css/
        │   └── styles.css   # Offline dark-theme design system
        └── js/
            ├── scanner.js   # Drag-and-drop file upload & scan UI logic
            └── dashboard.js # Repository table, stats counters & search logic
```

---

## ⚡ Quick Start Guide

### Prerequisites
- Python 3.10 or higher
- `git`
- Modern web browser (Chrome, Firefox, Edge, Safari)

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/nirikshan.git
cd nirikshan
```

### 2. Automated Setup

#### On Linux / macOS:
```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

#### On Windows:
```cmd
scripts\setup_env.bat
```

---

### Manual Setup (Alternative)

#### 1. Initialize Scaffolding
```bash
python scripts/init_project.py
```

#### 2. Create and Activate Virtual Environment
```bash
# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt
```

#### 4. Run the Application
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🐳 Docker Deployment

Nirikshan is fully containerized and includes all required OpenCV and EasyOCR runtime libraries:

```bash
# Navigate to docker directory and start container
cd docker
docker-compose up --build
```

The application will be accessible at:
- **Scanner UI**: [http://localhost:8000](http://localhost:8000)
- **Dashboard UI**: [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
- **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description | Request Format | Response Format |
|---|---|---|---|---|
| `GET` | `/` | Field Inspector Scanner Web UI | None | HTML |
| `GET` | `/dashboard` | Central Command Repository Web UI | None | HTML |
| `POST` | `/api/scan` | Primary label analysis and compliance scan | `multipart/form-data` (`file: image`) | `application/json` (Report, PDF & image links) |
| `GET` | `/api/repository` | Retrieve all historical scan records | None | `application/json` (Array of scan records) |
| `GET` | `/api/export-csv` | Download complete scan history as CSV | None | `text/csv` (Attachment download) |

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file or standard MIT terms for details.

```
MIT License

Copyright (c) 2026 Team Nirikshan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```
