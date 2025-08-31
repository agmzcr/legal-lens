from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

if TYPE_CHECKING:
    from app.models.user import User

class Document(SQLModel, table=True):
    __tablename__ = "documents"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    summary: str
    red_flags: list[str] = Field(default=[], sa_column=Column(JSON))
    clauses: list[dict] = Field(default=[], sa_column=Column(JSON))
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="documents")