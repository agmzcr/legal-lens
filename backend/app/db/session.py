from sqlmodel import Session, create_engine, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None, "DATABASE_URL must be set in .env"

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
