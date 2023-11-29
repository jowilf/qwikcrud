from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: Optional[str] = Field(None)
    openai_model: str = "gpt-3.5-turbo-1106"
    logging_level: str = "ERROR"


settings = Settings()
