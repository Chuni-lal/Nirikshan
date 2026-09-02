"""
Nirikshan — API Routes
Endpoints: /api/scan, /api/repository, /api/export-csv
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import uuid
import os
import shutil
from datetime import datetime

from app.core.config import UPLOADS_DIR, EVIDENCE_DIR, REPORTS_DIR, ALLOWED_EXTENSIONS
from app.core.database import save_scan_record, get_all_records

from app.vision.preprocessor import preprocess_image
from app.vision.ocr_engine import extract_text
from app.vision.font_analyzer import analyze_font_sizes
from app.rules.rule_evaluator import evaluate_compliance
from app.reports.pdf_builder import generate_pdf_report
from app.reports.csv_builder import generate_csv_export

router = APIRouter(prefix="/api", tags=["Compliance API"])


@router.post("/scan")
async def scan_product(
    file: UploadFile = File(...),
    custom_name: str = Form(None)
):
    """
    Upload a packaged commodity image for compliance scanning.
    Returns full compliance audit results.
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Upload JPG, PNG or WebP images only."
        )

    # Generate unique scan ID
    scan_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Determine final filename
    final_filename = custom_name.strip() if custom_name and custom_name.strip() else file.filename

    # Save uploaded file
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        file_ext = ".jpg"
    upload_path = os.path.join(UPLOADS_DIR, f"{scan_id}{file_ext}")

    with open(upload_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    try:
        # Step 1: Preprocess image
        processed_image = preprocess_image(upload_path)

        # Step 2: Extract text and bounding boxes via OCR
        ocr_results = extract_text(upload_path)

        # Step 3: Analyze font sizes
        font_analysis = analyze_font_sizes(ocr_results, upload_path)

        # Step 4: Evaluate compliance against legal rules
        compliance_report = evaluate_compliance(ocr_results, font_analysis)

        # Step 5: Generate evidence image with bounding boxes
        evidence_path = os.path.join(EVIDENCE_DIR, f"{scan_id}_evidence.jpg")
        # Copy original as evidence (bounding box overlay can be added later)
        shutil.copy2(upload_path, evidence_path)

        # Step 6: Generate PDF report
        pdf_path = os.path.join(REPORTS_DIR, f"{scan_id}_report.pdf")
        generate_pdf_report(scan_id, timestamp, compliance_report, upload_path, pdf_path)

        # Step 7: Save to database
        save_scan_record(scan_id, timestamp, final_filename, compliance_report)

        return {
            "scan_id": scan_id,
            "timestamp": timestamp,
            "filename": final_filename,
            "compliance_report": compliance_report,
            "pdf_report": f"/storage/generated_reports/{scan_id}_report.pdf",
            "evidence_image": f"/storage/evidence/{scan_id}_evidence.jpg"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@router.get("/repository")
async def get_repository():
    """Retrieve all past scan records from the database."""
    try:
        records = get_all_records()
        return {"total": len(records), "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch records: {str(e)}")


@router.get("/export-csv")
async def export_csv():
    """Export all compliance records as a downloadable CSV file."""
    try:
        csv_path = os.path.join(REPORTS_DIR, "compliance_export.csv")
        records = get_all_records()
        generate_csv_export(records, csv_path)
        return FileResponse(
            path=csv_path,
            filename="nirikshan_compliance_export.csv",
            media_type="text/csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")
