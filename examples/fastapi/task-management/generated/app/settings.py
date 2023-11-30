from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///db.sqlite"
    PROJECT_NAME: str = "Task Management"
    PROJECT_DESCRIPTION: str = (
        "An application for managing tasks with deadlines and assignees."
    )


settings = Settings()
