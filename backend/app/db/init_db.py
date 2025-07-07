from app.db.session import engine
from app.models.user import User
from app.models.document import Document
from sqlmodel import SQLModel

def init_db():
    SQLModel.metadata.create_all(engine)
