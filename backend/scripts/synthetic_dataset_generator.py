import os
import random
import math
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_synthetic_dataset(output_dir: str = "storage/synthetic_dataset", num_samples: int = 50):
    """
    Generates synthetic training samples of Indian packaged commodity declarations
    with realistic packaging distortions: dot-matrix printing, glare, curved surfaces, and noise.
    """
    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "annotations"), exist_ok=True)

    # Sample statutory templates based on PCR 2011 Rule 6(1)
    mrp_texts = ["MRP Rs. 150.00 (Incl. of all taxes)", "M.R.P. 249.00 INCL TAXES", "MAX RETAIL PRICE Rs 49.00"]
    net_qty_texts = ["Net Qty: 500 g", "NET WEIGHT 1.5 kg", "Net Volume: 750 ml", "CONTENTS: 250 g"]
    mfg_texts = ["PKD: 08/2026", "MFG DATE: 12/2025", "EXP: 24 MONTHS FROM MFG", "B.No. BATCH-2026-99A"]
    origin_texts = ["Country of Origin: India", "MADE IN INDIA", "ORIGIN: INDIA"]
    mfr_texts = ["Mfd by: Amul Dairy Fed, Anand 388001", "Packed by: Britannia Industries Ltd, KA"]
    care_texts = ["Customer Care: 1800-258-3333", "Email: care@consumer.gov.in"]

    bg_colors = [(240, 240, 240), (255, 250, 240), (220, 235, 252), (250, 240, 230)]
    text_colors = [(20, 20, 20), (10, 30, 80), (120, 20, 20), (10, 80, 20)]

    dataset_manifest = []

    for idx in range(num_samples):
        # Image canvas dimensions
        width, height = 640, 480
        bg_color = random.choice(bg_colors)
        img_pil = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img_pil)

        # Select font (fallback to default bitmap font if ttf unavailable)
        try:
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
            font_text = ImageFont.truetype("DejaVuSans.ttf", 18)
            font_small = ImageFont.truetype("DejaVuSansMono.ttf", 15)
        except Exception:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Build random statutory label block
        lines = [
            (random.choice(mrp_texts), font_title),
            (random.choice(net_qty_texts), font_text),
            (random.choice(mfg_texts), font_small),
            (random.choice(origin_texts), font_text),
            (random.choice(mfr_texts), font_small),
            (random.choice(care_texts), font_small)
        ]

        annotations = []
        y_cursor = random.randint(40, 70)

        for text, font in lines:
            text_color = random.choice(text_colors)
            x_pos = random.randint(30, 60)
            
            # Get text bounding box
            bbox = draw.textbbox((x_pos, y_cursor), text, font=font)
            draw.text((x_pos, y_cursor), text, fill=text_color, font=font)
            
            annotations.append({
                "text": text,
                "bbox": [
                    [bbox[0], bbox[1]],
                    [bbox[2], bbox[1]],
                    [bbox[2], bbox[3]],
                    [bbox[0], bbox[3]]
                ]
            })
            y_cursor += (bbox[3] - bbox[1]) + random.randint(12, 22)

        # Convert to OpenCV image format for packaging distortions
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # Apply synthetic packaging distortions:
        # 1. Specular Glare (Shiny plastic wrap)
        if random.random() > 0.4:
            overlay = img_cv.copy()
            cv2.circle(overlay, (random.randint(100, 500), random.randint(100, 400)), random.randint(80, 180), (255, 255, 255), -1)
            img_cv = cv2.addWeighted(img_cv, 0.8, overlay, 0.2, 0)

        # 2. Gaussian Noise & Blur
        if random.random() > 0.5:
            kernel_size = random.choice([3, 5])
            img_cv = cv2.GaussianBlur(img_cv, (kernel_size, kernel_size), 0)

        # 3. Cylindrical Label Warp (Curved packaging surfaces)
        if random.random() > 0.5:
            rows, cols = img_cv.shape[:2]
            map_x = np.zeros((rows, cols), np.float32)
            map_y = np.zeros((rows, cols), np.float32)
            for i in range(rows):
                for j in range(cols):
                    map_x[i, j] = j
                    map_y[i, j] = i + 10 * math.sin(j / 30.0)
            img_cv = cv2.remap(img_cv, map_x, map_y, cv2.INTER_LINEAR)

        # Save synthetic sample
        img_filename = f"sample_{idx+1:04d}.jpg"
        img_path = os.path.join(output_dir, "images", img_filename)
        cv2.imwrite(img_path, img_cv)

        ann_filename = f"sample_{idx+1:04d}.json"
        ann_path = os.path.join(output_dir, "annotations", ann_filename)
        with open(ann_path, "w", encoding="utf-8") as f:
            json.dump({"image": img_filename, "annotations": annotations}, f, indent=2)

        dataset_manifest.append({"image_path": img_path, "annotation_path": ann_path})

    print(f"✅ Generated {num_samples} synthetic packaging training samples in '{output_dir}'.")
    return dataset_manifest

if __name__ == "__main__":
    create_synthetic_dataset()
