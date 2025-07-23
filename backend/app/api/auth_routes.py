"""
Authentication Routes Module

Handles user registration and login processes.
Returns a JWT access token upon successful authentication.
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.auth.auth_handler import (
    SECRET_KEY,
    hash_password,
    verify_password,
    create_access_token,
)

# Initialize auth router with a prefix
router = APIRouter(prefix="/auth")

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """
    Registers a new user.

    - Validates that the email is not already in use.
    - Hashes the password before storing.
    - Returns a JWT access token.
    """
    # Check if user already exists
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create and persist new user
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token
    token = create_access_token({"sub": str(new_user.id)})
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticates user credentials.

    - Verifies email and password.
    - Returns a JWT access token on success.
    """
    # Fetch user by email
    db_user = session.exec(select(User).where(User.email == user.email)).first()

    # Validate credentials
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Generate JWT token
    token = create_access_token({"sub": str(db_user.id)})
    return TokenResponse(access_token=token)