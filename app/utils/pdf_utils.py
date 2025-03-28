from pdf2image import convert_from_bytes

def convert_pdf_to_png(file):
    images = convert_from_bytes(file.read(), dpi=300)
    return images[0]  # only first page