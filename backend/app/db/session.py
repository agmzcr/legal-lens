import os
import logging
from sqlmodel import create_engine, Session, SQLModel
from app.config import settings
from app.models.user import User
from app.models.document import Document

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL, echo=False)

def create_db_and_tables():
    """
    Creates the database tables based on SQLModel metadata.
    """
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Tables created successfully.")

def get_session():
    """
    FastAPI dependency to get a database session.
    """
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    create_db_and_tables()