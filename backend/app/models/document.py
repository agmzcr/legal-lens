from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str  # raw text
    summary: str
    red_flags: str  # JSON stringified
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
