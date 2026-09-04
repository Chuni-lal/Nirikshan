from typing import List, Dict, Any
from PIL import Image
from app.core.config import DEFAULT_DPI, FONT_SIZE_THRESHOLDS

def get_image_dpi(image_path: str) -> float:
    """
    Extract DPI from image metadata.
    Falls back to DEFAULT_DPI (300.0) if EXIF metadata is missing.
    """
    try:
        with Image.open(image_path) as img:
            dpi = img.info.get('dpi')
            if dpi is not None and dpi[0] > 0:
                return float(dpi[0])
    except Exception:
        pass
    return float(DEFAULT_DPI)

def calculate_font_size_mm(bbox_height_px: float, dpi: float, reference_ratio: float = 1.0) -> float:
    """
    Calculate physical font height in millimeters based on bounding box pixel height and DPI.
    Formula: (bbox_height_px / dpi) * 25.4 * reference_ratio
    Rule 6(1) requires measuring upper-case letter height.
    """
    height_mm = (bbox_height_px / dpi) * 25.4 * reference_ratio
    return round(height_mm, 2)

def get_bbox_height(bbox: List[List[float]]) -> float:
    """
    Calculate precise pixel height from a 4-corner bounding box.
    """
    top_left = bbox[0]
    bottom_left = bbox[3]
    top_right = bbox[1]
    bottom_right = bbox[2]
    
    left_height = abs(float(bottom_left[1]) - float(top_left[1]))
    right_height = abs(float(bottom_right[1]) - float(top_right[1]))
    return max(left_height, right_height)

def analyze_font_sizes(ocr_results: List[Dict[str, Any]], image_path: str, custom_dpi: float = None) -> List[Dict[str, Any]]:
    """
    Analyze font heights for extracted OCR text blocks against PCR 2011 Rule 6(1) thresholds.
    """
    dpi = custom_dpi if custom_dpi else get_image_dpi(image_path)
    min_required_mm = float(FONT_SIZE_THRESHOLDS.get('generic_declaration', 1.0))
    
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
