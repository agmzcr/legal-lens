from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    DatabaseError
)

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_user_service(db: Session = Depends(get_session)) -> UserService:
    """Provides an instance of UserService with a database session."""
    return UserService(db)

def get_auth_service(
    db: Session = Depends(get_session),
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    """Provides an instance of AuthService with a database session and a UserService instance."""
    return AuthService(db, user_service)


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Registers a new user, creates a refresh token, and returns an access token.
    """
    try:
        user = auth_service.register_user(user_data)
        tokens = auth_service.create_tokens_for_user(user.id)
        return tokens
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=Token,
    summary="Log in an existing user"
)
def login_for_access_token(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticates a user and returns access and refresh tokens.
    """
    try:
        user = auth_service.authenticate_user(user_data.email, user_data.password)
        tokens = auth_service.create_tokens_for_user(user.id)
        return tokens
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh an access token"
)
def refresh_access_token(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Refreshes the access token using a refresh token.
    """
    try:
        user_id = auth_service.verify_refresh_token(refresh_token)
        tokens = auth_service.create_tokens_for_user(user_id)
        return tokens
    except RefreshTokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )