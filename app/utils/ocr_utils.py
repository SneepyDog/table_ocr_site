import pytesseract
from PIL import Image
import layoutparser as lp


def extract_text_within_boxes(image_path, boxes):
    img = Image.open(image_path)
    ocr_data = pytesseract.image_to_data(img, lang="rus", output_type=pytesseract.Output.DICT)
    extracted = []

    for i in range(len(ocr_data['text'])):
        if int(ocr_data['conf'][i]) > 30:
            x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
            cx, cy = x + w // 2, y + h // 2
            for box in boxes:
                if box.contains(lp.Rectangle(x, y, x + w, y + h)):
                    extracted.append(ocr_data['text'][i])
                    break

    return " ".join(extracted)