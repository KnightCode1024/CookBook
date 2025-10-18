import os

from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    NAME: set = os.getenv("DB_NAME")
    HOST: str = os.getenv("DB_HOST")
    PORT: int = os.getenv("DB_PORT")
    USER: str = os.getenv("DB_USER")
    PASSWORD: str = os.getenv("DB_PASSWORD")

    def get_db_url(self):
        return (
            f"postgresql://{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/{self.NAME}"
        )


class AppConfig:
    HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    PORT: int = os.getenv("APP_PORT", 8080)
    DEBUG: bool = os.getenv("APP_DEBUG", False)
    SECRET_KEY: str = os.getenv("APP_SECRET_KEY")


class Config:
    DATABASE: DatabaseConfig = DatabaseConfig()
    APP: AppConfig = AppConfig()


config = Config()
