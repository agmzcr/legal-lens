"""
Authentication Dependency

Extracts and validates the current user from the Authorization header.
Used to protect routes that require authentication.
"""

from fastapi import Depends, HTTPException, Header
from jose import JWTError
from sqlmodel import Session, select

from app.auth.auth_handler import decode_token
from app.db.session import get_session
from app.models.user import User

def get_current_user(
    authorization: str = Header(...),
    session: Session = Depends(get_session)
) -> User:
    """
    Parses the Bearer token from the Authorization header,
    decodes it, and retrieves the authenticated user from the database.

    Raises:
        HTTPException: 401 if token is missing, invalid, or user is not found.

    Returns:
        User: Authenticated user instance
    """
    # Validate header format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid auth header"
        )

    # Extract token from "Bearer <token>"
    token = authorization[len("Bearer "):]

    try:
        # Decode token and extract user ID
        user_id = decode_token(token)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Look up user in the database
        user = session.exec(
            select(User).where(User.id == int(user_id))
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")