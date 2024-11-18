from pydantic_settings import BaseSettings # NEW


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
