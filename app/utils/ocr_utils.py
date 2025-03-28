import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import layoutparser as lp
import csv
import pandas as pd
import os


def extract_text_within_boxes(image_path, boxes):
    img = Image.open(image_path)
    ocr_data = pytesseract.image_to_data(img, lang="rus", output_type=pytesseract.Output.DICT)
    extracted = []

    for i in range(len(ocr_data['text'])):
        if int(ocr_data['conf'][i]) > 30:
            x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
            text_rect = lp.Rectangle(x, y, x + w, y + h)
            for box in boxes:
                if text_rect.is_in(box):
                    extracted.append(ocr_data['text'][i])
                    break

    return " ".join(extracted)


def save_results(text, output_dir, base_filename):

    base_filename = os.path.splitext(base_filename)[0]  # ← удалит .png
    txt_path = os.path.join(output_dir, f"{base_filename}.txt")

    base_filename = os.path.splitext(base_filename)[0]
    csv_path = os.path.join(output_dir, f"{base_filename}.csv")

    base_filename = os.path.splitext(base_filename)[0]
    xlsx_path = os.path.join(output_dir, f"{base_filename}.xlsx")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    # save CSV
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for line in text.split("\n"):
            writer.writerow([line])

    # save Excel
    df = pd.DataFrame([line.split("\t") for line in text.split("\n")])
    df.to_excel(xlsx_path, index=False, header=False)

    return {
        "txt": os.path.basename(txt_path),
        "csv": os.path.basename(csv_path),
        "xlsx": os.path.basename(xlsx_path)
    }


