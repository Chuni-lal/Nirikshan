import easyocr
import cv2
import re
import numpy as np
from typing import List, Dict, Any
from PIL import Image, ImageOps
from app.core.config import OCR_LANGUAGES, OCR_GPU

_reader = None

def get_reader() -> easyocr.Reader:
    """
    Lazy initialization of EasyOCR reader as a singleton.
    """
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(OCR_LANGUAGES, gpu=OCR_GPU)
    return _reader

def fix_exif_orientation(image_path: str):
    """
    Fix mobile camera EXIF orientation metadata before OCR.
    """
    try:
        with Image.open(image_path) as img:
            transposed = ImageOps.exif_transpose(img)
            transposed.save(image_path)
    except Exception:
        pass

def prepare_image_variants(image_path: str) -> List[np.ndarray]:
    """
    Creates high-resolution image variants to maximize OCR accuracy:
    1. Upscaled high-res color image (2x upscaling for small label fonts)
    2. High-contrast CLAHE grayscale image (for low lighting / shiny plastic glare)
    3. Morphologically closed Dot-Matrix variant (bridges inkjet printed dots into solid characters)
    """
    fix_exif_orientation(image_path)
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        return []

    h, w = img_bgr.shape[:2]
    
    # Scale up small images so fine font text (MRP, dates, net qty) becomes crisp
    if w < 1600 or h < 1600:
        scale = max(1600 / w, 1600 / h)
        img_bgr = cv2.resize(img_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

    # Variant 1: Grayscale CLAHE variant for shiny or low-contrast packaging
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    # Variant 2: Morphological Closing for Inkjet Dot-Matrix Printed Labels & Expiry Dates
    # Bridges isolated ink dots into continuous strokes before OCR
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dot_matrix_closed = cv2.morphologyEx(enhanced_gray, cv2.MORPH_CLOSE, kernel)

    return [img_bgr, enhanced_gray, dot_matrix_closed]

def normalize_ocr_text(text: str) -> str:
    """
    Sanitizes and normalizes raw OCR text to fix common dot-matrix print artifacts:
    - Normalizes rupee symbols (₹ -> Rs.)
    - Removes fragmented spaces inside numeric decimals (e.g. '150 . 00' -> '150.00')
    - Removes fragmented spaces in date expressions (e.g. '04 / 2026' -> '04/2026')
    - Fixes spaces around currency symbols (e.g. 'Rs . 150' -> 'Rs. 150')
    """
    if not text:
        return ""
    
    # Standardize Rupee symbol
    normalized = text.replace("₹", "Rs. ")
    
    # Fix broken decimal points in numeric amounts (e.g. 150 . 00 -> 150.00)
    normalized = re.sub(r'(\d+)\s*[\.,]\s*(\d{2})\b', r'\1.\2', normalized)
    
    # Fix broken slash in date expressions (e.g. 04 / 2026 -> 04/2026)
    normalized = re.sub(r'(\d{1,2})\s*/\s*(\d{2,4})', r'\1/\2', normalized)
    
    # Fix broken dot matrix spacing in MRP prefix (e.g. M . R . P . -> M.R.P.)
    normalized = re.sub(r'(?i)\bM\s*[\.,]\s*R\s*[\.,]\s*P\b', 'M.R.P.', normalized)
    
    # Fix broken dot matrix spacing in RS prefix (e.g. R\s*s\s*\. -> Rs.)
    normalized = re.sub(r'(?i)\bR\s*s\s*[\.,]', 'Rs.', normalized)

    # Clean multiple spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized

def merge_text_blocks_into_lines(ocr_raw_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Groups OCR bounding box tokens by vertical alignment and horizontal proximity
    to reconstruct complete statutory lines without merging far-apart columns.
    """
    if not ocr_raw_results:
        return []

    # Calculate bounding box info for each token
    items = []
    for item in ocr_raw_results:
        bbox = item['bbox']
        top_y = min(pt[1] for pt in bbox)
        bottom_y = max(pt[1] for pt in bbox)
        left_x = min(pt[0] for pt in bbox)
        right_x = max(pt[0] for pt in bbox)
        height = max(bottom_y - top_y, 10)
        y_center = (top_y + bottom_y) / 2.0
        items.append({
            "bbox": bbox,
            "text": item['text'],
            "confidence": item['confidence'],
            "y_center": y_center,
            "left_x": left_x,
            "right_x": right_x,
            "height": height
        })

    # Sort tokens top-to-bottom, then left-to-right
    items.sort(key=lambda x: (x['y_center'], x['left_x']))

    clusters = []
    
    for item in items:
        placed = False
        for cluster in clusters:
            avg_y = sum(i['y_center'] for i in cluster) / len(cluster)
            avg_h = sum(i['height'] for i in cluster) / len(cluster)
            
            # Check if token is vertically aligned with cluster (within 40% height)
            if abs(item['y_center'] - avg_y) <= (avg_h * 0.40):
                # Check horizontal gap: only merge if token is adjacent (gap <= 2.5x font height)
                cluster_right_x = max(i['right_x'] for i in cluster)
                horizontal_gap = item['left_x'] - cluster_right_x
                
                if -20 <= horizontal_gap <= max(avg_h * 2.5, 60):
                    cluster.append(item)
                    placed = True
                    break
        if not placed:
            clusters.append([item])

    merged_results = []
    for cluster in clusters:
        cluster.sort(key=lambda x: x['left_x'])
        merged_text = " ".join(i['text'] for i in cluster)
        merged_text = normalize_ocr_text(merged_text)
        avg_conf = sum(i['confidence'] for i in cluster) / len(cluster)
        
        min_x = min(min(pt[0] for pt in i['bbox']) for i in cluster)
        min_y = min(min(pt[1] for pt in i['bbox']) for i in cluster)
        max_x = max(max(pt[0] for pt in i['bbox']) for i in cluster)
        max_y = max(max(pt[1] for pt in i['bbox']) for i in cluster)
        
        merged_results.append({
            "bbox": [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]],
            "text": merged_text.strip(),
            "confidence": round(avg_conf, 4)
        })

    return merged_results

def extract_text(image_path: str) -> List[Dict[str, Any]]:
    """
    Extract text from packaging image using EasyOCR with:
    - Multi-variant resolution upscaling & contrast enhancement
    - Dot-Matrix morphological closing for inkjet printed text/dates
    - Token confidence filtering & text normalization
    - Proximity-based line reconstruction
    """
    reader = get_reader()
    variants = prepare_image_variants(image_path)
    if not variants:
        return []

    raw_results = []
    seen_texts = set()

    for var in variants:
        try:
            results = reader.readtext(var, detail=1)
            for (bbox, text, prob) in results:
                clean_text = normalize_ocr_text(text)
                if clean_text and float(prob) >= 0.20:
                    if clean_text.lower() not in seen_texts:
                        raw_results.append({
                            "bbox": bbox,
                            "text": clean_text,
                            "confidence": round(float(prob), 4)
                        })
                        seen_texts.add(clean_text.lower())
        except Exception:
            pass

    # Merge proximate tokens into coherent declaration phrases
    merged_lines = merge_text_blocks_into_lines(raw_results)
    
    # Combine both individual distinct tokens and merged phrases for maximum rule detection
    combined_results = list(merged_lines)
    for raw in raw_results:
        if raw['text'].lower() not in [m['text'].lower() for m in merged_lines]:
            combined_results.append(raw)
            
    return combined_results
