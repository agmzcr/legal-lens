from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    summary: str
    red_flags: str
    clauses: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
