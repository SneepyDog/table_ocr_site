from PIL import Image
import cv2
import numpy as np

def process_image_crop_rotate(src_path, dst_path, crop, rotate):
    img = Image.open(src_path)
    x, y, w, h = crop["x"], crop["y"], crop["width"], crop["height"]
    cropped = img.crop((x, y, x + w, y + h))

    if rotate == 90:
        cropped = cropped.rotate(-90, expand=True)
    elif rotate == -90:
        cropped = cropped.rotate(90, expand=True)

    cropped.save(dst_path)