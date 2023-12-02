from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///db.sqlite"
    PROJECT_NAME: str = "TaskManager"
    PROJECT_DESCRIPTION: str = "An application for managing tasks that enables multiple users to collaborate on a single project with multiple tasks."


settings = Settings()
