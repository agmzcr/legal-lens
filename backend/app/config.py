from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


    ENVIRONMENT: str
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    LLM_MODEL: str
    DATABASE_URL: str

    PASSWORD_MIN_LENGTH: int
    PASSWORD_REQUIRE_UPPER: bool
    PASSWORD_REQUIRE_LOWER: bool
    PASSWORD_REQUIRE_DIGIT: bool
    PASSWORD_REQUIRE_SPECIAL: bool

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int

    JWT_REFRESH_SECRET_KEY: str
    JWT_REFRESH_TOKEN_EXPIRES_MINUTES: int

settings = Settings()