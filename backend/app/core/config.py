import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

STORAGE_DIR = os.path.join(BASE_DIR, "storage")
UPLOADS_DIR = os.path.join(STORAGE_DIR, "uploads")
EVIDENCE_DIR = os.path.join(STORAGE_DIR, "evidence")
REPORTS_DIR = os.path.join(STORAGE_DIR, "generated_reports")
DATABASE_PATH = os.path.join(STORAGE_DIR, "nirikshan.db")

OCR_LANGUAGES = ["en", "hi"]
OCR_GPU = False
DEFAULT_DPI = 300
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

FONT_SIZE_THRESHOLDS = {
    "net_quantity": {
        "area_<=_100_cm2": 1.0,
        "area_100-500_cm2": 2.0,
        "area_500-2500_cm2": 4.0,
        "area_>_2500_cm2": 6.0,
    },
    "mrp": 2.0,
    "generic_declaration": 1.0,
}
