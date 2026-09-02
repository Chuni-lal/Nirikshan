from typing import List, Dict, Any
from PIL import Image
from app.core.config import DEFAULT_DPI, FONT_SIZE_THRESHOLDS

def get_image_dpi(image_path: str) -> float:
    """
    Extract DPI from image metadata.
    Falls back to DEFAULT_DPI if not found.
    """
    try:
        with Image.open(image_path) as img:
            dpi = img.info.get('dpi')
            if dpi is not None:
                return float(dpi[0])
    except Exception:
        pass
    return float(DEFAULT_DPI)

def calculate_font_size_mm(bbox_height_px: float, dpi: float) -> float:
    """
    Calculate font size in millimeters based on pixel height and DPI.
    Formula: (bbox_height_px / dpi) * 25.4
    """
    return round((bbox_height_px / dpi) * 25.4, 2)

def get_bbox_height(bbox: List[List[float]]) -> float:
    """
    Calculate pixel height from a 4-corner bounding box.
    """
    top_left = bbox[0]
    bottom_left = bbox[3]
    return abs(float(bottom_left[1]) - float(top_left[1]))

def analyze_font_sizes(ocr_results: List[Dict[str, Any]], image_path: str) -> List[Dict[str, Any]]:
    """
    Analyze font sizes for all OCR results and check compliance against generic declaration threshold.
    """
    dpi = get_image_dpi(image_path)
    min_required_mm = float(FONT_SIZE_THRESHOLDS['generic_declaration'])
    
    analysis = []
    for result in ocr_results:
        bbox = result['bbox']
        text = result['text']
        bbox_height_px = get_bbox_height(bbox)
        font_size_mm = calculate_font_size_mm(bbox_height_px, dpi)
        is_compliant = font_size_mm >= min_required_mm
        
        analysis.append({
            "text": text,
            "bbox": bbox,
            "bbox_height_px": round(bbox_height_px, 2),
            "dpi": dpi,
            "font_size_mm": font_size_mm,
            "min_required_mm": min_required_mm,
            "is_compliant": is_compliant
        })
    return analysis
