from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class Configs(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH,
        env_file_encoding="utf-8"
    )

    DATABASE_URL: str = ""

configs = Configs()
