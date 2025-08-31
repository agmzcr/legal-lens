from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose.exceptions import ExpiredSignatureError, JWTError

from app.db.session import get_session
from app.services.jwt import jwt_service
from app.services.user_service import UserService
from app.services.document_service import DocumentService
from app.services.ai_engine import AIEngineService
from app.services.pdf_parser import PDFParserService
from app.models.user import User
from app.models.document import Document
from app.core.exceptions import DatabaseError, DocumentNotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user_service(db: Session = Depends(get_session)) -> UserService:
    """Provides an instance of the UserService."""
    return UserService(db)

def get_ai_engine_service() -> AIEngineService:
    """Provides an instance of the AIEngineService."""
    return AIEngineService()

def get_pdf_parser_service() -> PDFParserService:
    """Provides an instance of the PDFParserService."""
    return PDFParserService()

def get_document_service(
    db: Session = Depends(get_session),
    pdf_parser_service: PDFParserService = Depends(get_pdf_parser_service),
    ai_engine_service: AIEngineService = Depends(get_ai_engine_service)
) -> DocumentService:
    """Provides an instance of the DocumentService."""
    return DocumentService(db, pdf_parser_service, ai_engine_service)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    FastAPI dependency to get the current user from a JWT token.
    """
    try:
        payload = jwt_service.verify_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during token validation."
        )

    try:
        user = user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    return user

def document_or_404(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_document_service)
) -> Document:
    """
    FastAPI dependency to get a user's document or raise a 404 error.
    """
    try:
        document = doc_service.get_document_by_id(doc_id, current_user.id)
        return document
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))