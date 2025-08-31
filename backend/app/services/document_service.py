import json
import logging
from typing import Generator
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.document import Document
from app.services.pdf_parser import PDFParserService
from app.services.ai_engine import AIEngineService
from app.core.exceptions import (
    PDFParseError,
    AIEngineError,
    DocumentNotFoundError,
    DatabaseError,
    UnsupportedFileTypeError,
)

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(
        self,
        db: Session,
        pdf_parser_service: PDFParserService,
        ai_engine_service: AIEngineService,
    ):
        self.db = db
        self.pdf_parser_service = pdf_parser_service
        self.ai_engine_service = ai_engine_service

    def create_document(self, file: UploadFile, user_id: int) -> Document:
        """
        Processes a file, analyzes its content, and creates a new document.
        """
        if file.content_type != "application/pdf":
            raise UnsupportedFileTypeError("Only PDFs are supported.")

        try:
            file.file.seek(0)
            text_generator: Generator[str, None, None] = self.pdf_parser_service.extract_text(file.file)
            file_content = "".join(text_generator)
        except PDFParseError as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise e
        
        try:
            analysis = self.ai_engine_service.analyze_text_with_ai(file_content)
        except AIEngineError as e:
            logger.error(f"AI engine service unavailable: {e}")
            raise e
        
        document = Document(
            title=file.filename,
            content=file_content,
            summary=analysis.get("summary"),
            red_flags=analysis.get("red_flags", []),
            clauses=analysis.get("clauses", []),
            user_id=user_id,
        )

        try:
            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)
            return document
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error creating document for user {user_id}: {e}")
            raise DatabaseError("Error saving the document.")

    def get_document_by_id(self, doc_id: int, user_id: int) -> Document:
        """
        Retrieves a document by its ID and ensures it belongs to the user.
        """
        try:
            document = self.db.query(Document).filter(
                Document.id == doc_id,
                Document.user_id == user_id,
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching document {doc_id} for user {user_id}: {e}")
            raise DatabaseError("Error fetching document.")

        if not document:
            raise DocumentNotFoundError("Document not found.")

        return document

    def list_documents_for_user(self, user_id: int) -> list[Document]:
        """
        Lists all documents for a given user.
        """
        try:
            documents = self.db.query(Document).filter(Document.user_id == user_id).all()
            return documents
        except SQLAlchemyError as e:
            logger.error(f"Database error listing documents for user {user_id}: {e}")
            raise DatabaseError("Error listing documents.")

    def delete_document(self, doc_id: int, user_id: int) -> None:
        """
        Deletes a document by its ID, ensuring it belongs to the user.
        """
        try:
            document = self.get_document_by_id(doc_id, user_id)
            self.db.delete(document)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error deleting document {doc_id} for user {user_id}: {e}")
            raise DatabaseError("Error deleting document.")