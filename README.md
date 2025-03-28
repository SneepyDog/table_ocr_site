❌ Не работает :( ❌

## === README.md ===

# Table OCR App

Простое локальное веб-приложение для распознавания таблиц с изображений и PDF-документов. Использует связку LayoutParser + Tesseract для точного определения структуры таблиц и распознавания текста на русском языке.

---

## Быстрый старт

### 1. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

Также убедитесь, что установлен Tesseract OCR:
- Linux: `sudo apt install tesseract-ocr`
- Mac: `brew install tesseract`
- Windows: [скачать здесь](https://github.com/tesseract-ocr/tesseract)

Проверьте, что Tesseract работает:
```bash
tesseract --version
```

### 2. Запуск приложения
```bash
python app.py
```

Приложение будет доступно по адресу: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Как использовать
1. Загрузите PDF или изображение (PNG, JPEG).
2. Отметьте нужную область (в текущей версии — фиксированная область, автообрезка в коде).
3. Поверните изображение при необходимости.
4. Нажмите "Распознать".
5. Скачайте результат в `.txt` формате.

---

## Используемые технологии
- Flask (бэкенд)
- JavaScript + HTML (интерфейс)
- LayoutParser + Detectron2 (распознавание структуры таблиц)
- PyTesseract (OCR с поддержкой русского языка)
- PDF2Image (конвертация PDF в изображение)
- Pillow/OpenCV (обработка изображений)

---

## Структура проекта
```
table-ocr-app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── utils/
│       ├── pdf_utils.py
│       ├── image_utils.py
│       ├── layout_utils.py
│       └── ocr_utils.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── uploads/           # Временные файлы (создается автоматически)
├── app.py             # Точка входа
├── requirements.txt
└── README.md
```

---

## Примечания
- Поддерживаются только одностраничные PDF
- Область обрезки пока зашита в код (можно сделать drag-n-drop позже)
- Tesseract должен быть установлен отдельно

---

Готово к запуску — остаётся только скормить картинку :)
