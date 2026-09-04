import cv2
import numpy as np
from PIL import Image, ImageOps

def fix_exif_orientation(image_path: str):
    """
    Auto-rotates image according to EXIF orientation metadata tags
    (e.g., mobile camera portrait/tilted shots).
    """
    try:
        with Image.open(image_path) as img:
            transposed = ImageOps.exif_transpose(img)
            transposed.save(image_path)
    except Exception:
        pass

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess image for EasyOCR:
    1. Fix EXIF orientation (mobile phone portrait/upside-down shots)
    2. Read image
    3. Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) for low lighting/glare
    4. Apply subtle Bilateral Filter to remove noise while preserving sharp font edges
    """
    fix_exif_orientation(image_path)
    
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot load image at path: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Contrast enhancement for low lighting / shiny plastic reflections
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)
    
    # Bilateral filter to smooth background noise while keeping text boundaries sharp
    filtered = cv2.bilateralFilter(contrast_enhanced, 5, 50, 50)
    
    return filtered
