from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = "../env"
        
settings = Settings()