from fastapi import Depends, HTTPException, Header
from jose import JWTError
from app.auth.auth_handler import decode_token
from app.models.user import User
from app.db.session import get_session
from sqlmodel import Session, select

def get_current_user(
    authorization: str = Header(...),
    session: Session = Depends(get_session)
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization[7:]
    try:
        user_id = decode_token(token)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = session.exec(select(User).where(User.id == int(user_id))).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")
