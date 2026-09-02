import cv2
import numpy as np

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess an image for OCR.
    - Loads image
    - Converts to grayscale
    - Applies bilateral filter
    - Applies adaptive threshold
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot load image at path: {image_path}")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    return thresh
