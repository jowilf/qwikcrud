from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///db.sqlite"
    PROJECT_NAME: str = "Task Manager"
    PROJECT_DESCRIPTION: str = "An application for managing tasks and collaboration."


settings = Settings()
