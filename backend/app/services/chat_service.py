import logging
from typing import Dict
from sqlalchemy.orm import Session
from app.models.document import Document
from app.services.ai_engine import AIEngineService
from app.services.document_service import DocumentService
from app.core.exceptions import DocumentNotFoundError, AIEngineError

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(
        self,
        db: Session,
        ai_engine_service: AIEngineService,
        document_service: DocumentService
    ):
        self.db = db
        self.ai_engine_service = ai_engine_service
        self.document_service = document_service

    def get_chat_response(self, document_id: int, user_id: int, message: str) -> Dict[str, str]:
        """
        Retrieves a contextual response from the AI for a given document.
        """
        try:
            document = self.document_service.get_document_by_id(document_id, user_id)
        except DocumentNotFoundError:
            logger.warning(f"Attempt to chat on non-existent or unauthorized document_id={document_id} by user_id={user_id}")
            raise DocumentNotFoundError("Document not found or user not authorized.")

        context_prompt = (
            f"You are a legal assistant. Your task is to provide concise and accurate answers based on the provided legal document analysis. "
            f"The document is titled '{document.title}'. Here is the key information:\n\n"
            f"SUMMARY: {document.summary}\n\n"
            f"RED FLAGS: {document.red_flags}\n\n"
            f"CLAUSES: {document.clauses}\n\n"
            f"Based on this context, answer the user's question: '{message}'"
        )

        try:
            response = self.ai_engine_service.get_ai_response(
            text=document.content,
            question=message
        )

            return {"response": response}
        except AIEngineError as e:
            logger.error(f"AI engine service failed for chat query on document {document_id}: {e}")
            raise AIEngineError("AI chat service is unavailable.")