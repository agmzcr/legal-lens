from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.auth.auth_handler import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return TokenResponse(access_token=token)
