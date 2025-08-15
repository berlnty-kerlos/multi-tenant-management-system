print("Loading settings...")  # Debugging line
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pathlib import Path

env_file = ".env"
if os.getenv("ENVIRONMENT") == "test":
    env_file = ".env.test"

load_dotenv(Path(__file__).resolve().parents[3]  / env_file)

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = env_file

settings = Settings()