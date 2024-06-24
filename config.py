from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    telegram_token: str
    openai_api_key: str
    amplitude_api_key: str

    class Config:
        env_file = "../.env"


settings = Settings()
