import logging
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.document_service import DocumentService
from app.services.pdf_parser import PDFParserService
from app.services.ai_engine import AIEngineService
from app.schemas.document import DocumentSummary, DocumentListItem, DocumentCreate
from app.models.user import User
from app.core.exceptions import (
    DocumentNotFoundError,
    DatabaseError,
    UnsupportedFileTypeError,
    PDFParseError,
    AIEngineError,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])

def get_document_service(
    db: Session = Depends(get_session),
    pdf_parser_service: PDFParserService = Depends(PDFParserService),
    ai_engine_service: AIEngineService = Depends(AIEngineService)
) -> DocumentService:
    """Provides an instance of DocumentService with its dependencies."""
    return DocumentService(db, pdf_parser_service, ai_engine_service)

@router.post(
    "/",
    response_model=DocumentSummary,
    status_code=status.HTTP_201_CREATED,
    summary="Add an analyzed document"
)
def add_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_document_service)
):
    """
    Processes a PDF document, analyzes it, and saves it for the current user.
    """
    try:
        document = doc_service.create_document(file, current_user.id)
        return DocumentSummary.model_validate(document)
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(e))
    except (PDFParseError, AIEngineError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        logger.error(f"Unexpected error in add_document: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.get(
    "/{doc_id}",
    response_model=DocumentSummary,
    summary="Get document details"
)
def read_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_document_service)
):
    """
    Retrieves a single document by its ID if it belongs to the current user.
    """
    try:
        document = doc_service.get_document_by_id(doc_id, current_user.id)
        return DocumentSummary.model_validate(document)
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get(
    "/",
    response_model=list[DocumentListItem],
    summary="List user documents"
)
def list_documents(
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_document_service)
):
    """
    Lists all documents belonging to the current user.
    """
    try:
        documents = doc_service.list_documents_for_user(current_user.id)
        return [DocumentListItem.model_validate(doc) for doc in documents]
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete(
    "/{doc_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Delete document"
)
def delete_document_by_id(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_document_service)
):
    """
    Deletes a document by its ID if it belongs to the current user.
    """
    try:
        doc_service.delete_document(doc_id, current_user.id)
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")