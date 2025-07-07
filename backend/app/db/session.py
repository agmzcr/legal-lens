import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, SQLModel

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=dotenv_path)

print("✅ ENVIRONMENT =", os.getenv("ENVIRONMENT"))
print("✅ DATABASE_URL =", os.getenv("DATABASE_URL"))
print("✅ OPENROUTER_API_KEY =", os.getenv("OPENROUTER_API_KEY"))

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None, "DATABASE_URL must be set in .env"

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
