from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DocumentSummary(BaseModel):
    id: int
    title: str
    content: str
    summary: str
    red_flags: List[str]
    clauses: List[dict]
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DocumentListItem(BaseModel):
    id: int
    title: str
    summary: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DocumentCreate(BaseModel):
    title: str