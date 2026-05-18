import io
from PIL import Image
import pytesseract
from pypdf import PdfWriter, PdfReader


def images_to_searchable_pdf(image_sources, lang='eng'):
    """Convert a list of image file paths or file-like objects to a single searchable PDF."""
    writer = PdfWriter()
    for src in image_sources:
        img = Image.open(src)
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension='pdf', lang=lang)
        writer.append(PdfReader(io.BytesIO(pdf_bytes)))
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
