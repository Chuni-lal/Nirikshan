import easyocr
from typing import List, Dict, Any
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

def extract_text(image_path: str) -> List[Dict[str, Any]]:
    """
    Extract text and bounding boxes from an image using EasyOCR.
    """
    reader = get_reader()
    results = reader.readtext(image_path, detail=1)
    
    formatted_results = []
    for (bbox, text, prob) in results:
        formatted_results.append({
            "bbox": bbox,
            "text": text.strip(),
            "confidence": round(float(prob), 4)
        })
    return formatted_results
