import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.user import UserCreate
from app.schemas.token import Token
from app.config import settings
from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    DatabaseError
)
from app.services.jwt import jwt_service
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session, user_service: UserService):
        self.db = db
        self.user_service = user_service

    def register_user(self, user_in: UserCreate) -> User:
        """
        Registers a new user after checking if the email is already in use.
        """
        existing_user = self.user_service.get_user_by_email(user_in.email)
        if existing_user:
            raise UserAlreadyExistsError("Email is already registered.")

        hashed_password = pwd_context.hash(user_in.password)
        user_in.password = hashed_password
        
        try:
            user = self.user_service.create_user(user_in)
            return user
        except DatabaseError as e:
            raise e

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticates a user by email and password.
        """
        user = self.user_service.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password.")
        
        return user
    
    def create_tokens_for_user(self, user_id: int) -> Token:
        """
        Generates new access and refresh tokens for a user.
        """
        access_token = jwt_service.create_access_token(data={"sub": str(user_id)})
        refresh_token_string = self.create_and_store_refresh_token(user_id)
        return Token(access_token=access_token, refresh_token=refresh_token_string)

    def verify_refresh_token(self, refresh_token_string: str) -> int:
        """
        Verifies a refresh token against the database and returns the user ID.
        """
        try:
            stored_token = self.db.query(RefreshToken).filter(
                RefreshToken.token == refresh_token_string,
                RefreshToken.revoked == False
            ).first()

            if not stored_token:
                raise RefreshTokenExpiredError("Invalid refresh token or already revoked.")
                
            if stored_token.expires_at < datetime.utcnow():
                self.revoke_refresh_token(stored_token)
                raise RefreshTokenExpiredError("Expired refresh token.")
            
            return stored_token.user_id
        except SQLAlchemyError as e:
            logger.error(f"Database error verifying refresh token: {e}", exc_info=True)
            raise DatabaseError("Error verifying refresh token.")

    def create_and_store_refresh_token(self, user_id: int) -> str:
        """
        Creates a refresh token and stores it in the database.
        """
        token_string = jwt_service.create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRES_MINUTES)
        )
        
        expires_at = datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRES_MINUTES)
        
        try:
            new_token = RefreshToken(
                token=token_string,
                user_id=user_id,
                expires_at=expires_at
            )
            self.db.add(new_token)
            self.db.commit()
            self.db.refresh(new_token)
            return new_token.token
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error storing refresh token for user {user_id}: {e}", exc_info=True)
            raise DatabaseError("Error storing refresh token.")

    def revoke_refresh_token(self, rt: RefreshToken) -> None:
        """
        Revokes a refresh token by marking it as revoked in the database.
        """
        try:
            rt.revoked = True
            self.db.add(rt)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error revoking refresh token {rt.id}: {e}", exc_info=True)
            raise DatabaseError("Error revoking refresh token.")
            
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain-text password against a hashed one.
        """
        return pwd_context.verify(plain_password, hashed_password)