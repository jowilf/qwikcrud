import logging
from typing import Any, Dict, List

from openai import OpenAI

from qwikcrud.helpers import path_to
from qwikcrud.provider.base import AIProvider
from qwikcrud.schemas import App
from qwikcrud.settings import settings


class OpenAIProvider(AIProvider):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=settings.openai_api_key)
        with open(path_to("prompts/system")) as f:
            system_message = f.read()
        self.messages: List[Dict[str, Any]] = [
            {
                "role": "system",
                "content": system_message,
            },
        ]

    def get_name(self) -> str:
        return f"ChatGPT ({settings.openai_model})"

    def query(self, prompt: str) -> App:
        self.messages.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            response_format={"type": "json_object"},
            messages=self.messages,
            temperature=0.4,
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.content,
            }
        )
        logging.debug(
            f"Result from {self.get_name()}: {completion.choices[0].message.content}"
        )
        return App.model_validate_json(
            completion.choices[0].message.content, strict=False
        )
