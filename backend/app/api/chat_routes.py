import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.services.chat_service import ChatService
from app.services.ai_engine import AIEngineService
from app.services.document_service import DocumentService
from app.api.deps import get_current_user, get_document_service, get_ai_engine_service
from app.models.user import User
from app.schemas.ai_chat import ChatRequest, ChatResponse
from app.core.exceptions import DocumentNotFoundError, AIEngineError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
def get_chat_response(
    request: ChatRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_session),
    ai_engine_service: AIEngineService = Depends(get_ai_engine_service),
    document_service: DocumentService = Depends(get_document_service),
):
    """
    Retrieves a contextual response from the AI for a given document.
    """
    chat_service = ChatService(
        db=db,
        ai_engine_service=ai_engine_service,
        document_service=document_service
    )
    
    try:
        response = chat_service.get_chat_response(
            document_id=request.document_id,
            user_id=current_user.id,
            message=request.message
        )
        return ChatResponse(response=response["response"])
    except DocumentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except AIEngineError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
