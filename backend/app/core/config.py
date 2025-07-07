import os
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path)

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")

settings = Settings()
