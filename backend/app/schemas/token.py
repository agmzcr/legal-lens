from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str
    exp: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class TokenRefresh(BaseModel):
    refresh_token: str
