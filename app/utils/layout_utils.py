from paddleocr import PaddleOCR
from PIL import Image
import layoutparser as lp

ocr_model = PaddleOCR(use_angle_cls=True, lang='ru', use_gpu=False, show_log=False, det_db_box_thresh=0.5)

def detect_tables(image_path):
    try:
        result = ocr_model.ocr(image_path, cls=False)
        boxes = []

        for line in result:
            for box, (_text, _conf) in line:
                x1, y1 = map(int, box[0])
                x2, y2 = map(int, box[2])
                rect = lp.Rectangle(x1, y1, x2, y2)
                boxes.append(rect)

        return boxes

    except Exception as e:
        print("[ERROR] Не удалось выполнить обнаружение таблиц через PaddleOCR:", e)
        raise RuntimeError("Ошибка PaddleOCR при обнаружении структуры таблицы")
