from pydantic import BaseModel
from typing import List, Dict

class Clause(BaseModel):
    title: str
    content: str

class DocumentAnalysis(BaseModel):
    summary: str
    clauses: List[Clause]
    red_flags: List[str]
