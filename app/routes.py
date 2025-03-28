from flask import Blueprint, render_template, request, send_file, jsonify, current_app
import os
import uuid
from .utils.pdf_utils import convert_pdf_to_png
from .utils.image_utils import process_image_crop_rotate
from .utils.layout_utils import detect_tables
from .utils.ocr_utils import extract_text_within_boxes

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Файл не найден"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Файл не выбран"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4()}.png"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    try:
        if ext == ".pdf":
            img = convert_pdf_to_png(file)
            img.save(filepath)
        else:
            file.save(filepath)
        print(f"[INFO] Файл сохранён: {filepath}")
        return jsonify({"filename": filename})
    except Exception as e:
        print(f"[ERROR] Ошибка при сохранении: {e}")
        return jsonify({"error": str(e)}), 500

@main.route("/process", methods=["POST"])
def process():
    data = request.json
    filename = data["filename"]
    crop = data["crop"]  # {x, y, width, height}
    rotate = data["rotate"]

    upload_folder = current_app.config['UPLOAD_FOLDER']
    img_path = os.path.join(upload_folder, filename)
    processed_path = os.path.join(upload_folder, f"processed_{filename}")

    process_image_crop_rotate(img_path, processed_path, crop, rotate)

    tables = detect_tables(processed_path)
    result_text = extract_text_within_boxes(processed_path, tables)

    result_file = os.path.join(upload_folder, f"{filename}.txt")
    with open(result_file, "w", encoding="utf-8") as f:
        f.write(result_text)

    return jsonify({"result_file": f"{filename}.txt"})

@main.route("/download/<path:filename>")
def download(filename):
    return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    folder = os.path.abspath(current_app.config['UPLOAD_FOLDER'])
    path = os.path.join(folder, filename)
    if not os.path.isfile(path):
        return f"Файл {filename} не найден", 404
    return send_file(path)
