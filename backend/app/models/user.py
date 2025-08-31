from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from app.models.document import Document
from app.models.refresh_token import RefreshToken

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    refresh_tokens: list["RefreshToken"] = Relationship(back_populates="user")
    documents: list["Document"] = Relationship(back_populates="user")


