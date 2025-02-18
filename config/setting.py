from dotenv import load_dotenv

import os
from typing import Optional
from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

""" print("Current Working Directory:", os.getcwd())
print("Path to .env file:", os.path.abspath('../.env'))
print("DATABASE_URL:", os.getenv('DATABASE_URL')) """

class Settings(BaseSettings):
    DATABASE_URL: str
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: Optional[PositiveInt] = None
    EMAIL_USER: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    class Config:        
        env_ignore_empty = True
        model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')
        
settings = Settings()

