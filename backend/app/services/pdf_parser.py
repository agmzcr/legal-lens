import fitz
import logging
from typing import Generator
from io import BytesIO
from app.core.exceptions import PDFParseError

logger = logging.getLogger(__name__)

class PDFParserService:
    def extract_text(self, pdf_file) -> Generator[str, None, None]:
        """
        Extracts text from each page of a PDF file.
        Yields a string for each page.
        """
        try:
            pdf_bytes = pdf_file.read()
            pdf_stream = BytesIO(pdf_bytes)

            with fitz.open(stream=pdf_stream, filetype="pdf") as doc:
                for page in doc:
                    text = page.get_text()
                    yield text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}", exc_info=True)
            raise PDFParseError("Could not extract text from PDF. The file may be corrupted or unreadable.")