import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class DbSettings(BaseModel):
    db_user: str = os.getenv("POSTGRES_USER")
    db_password: str = os.getenv("POSTGRES_PASSWORD")
    db_server: str = os.getenv("POSTGRES_SERVER", "localhost")
    db_port: str = os.getenv("POSTGRES_PORT", 5432)
    db_name: str = os.getenv("POSTGRES_DB", "name")
    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
    db_echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()


settings = Settings()
