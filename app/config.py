from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    ALGORITHM: str = "HS256"
    DB_PORT: str
    DB_NAME: str
    DB_URL: str
    SECRET_KEY: str
    ADMIN_EMAIL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()