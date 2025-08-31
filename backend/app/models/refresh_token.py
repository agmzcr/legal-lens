from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User

class RefreshToken(SQLModel, table=True):
    token: str = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    revoked: bool = Field(default=False)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="refresh_tokens")