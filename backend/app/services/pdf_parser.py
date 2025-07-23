import fitz
from typing import Union
from io import BytesIO

def extract_text_from_pdf(pdf_bytes: Union[bytes, BytesIO]) -> str:
    """
    Extract raw text from PDF bytes using PyMuPDF.
    """
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text
