import logging
from typing import Any

import google.generativeai as genai

import qwikcrud.helpers as h
from qwikcrud.provider.base import AIProvider
from qwikcrud.schemas import App
from qwikcrud.settings import settings


class GoogleProvider(AIProvider):
    def __init__(self):
        super().__init__()
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.google_model)
        with open(h.path_to("prompts/system")) as f:
            system_message = f.read()
        self.messages: list[dict[str, Any]] = [
            {
                "role": "user",
                "parts": [system_message],
            },
            {
                "role": "model",
                "parts": ["OK"],
            },
        ]

    def get_name(self) -> str:
        return f"Google ({settings.google_model})"

    def query(self, prompt: str) -> App:
        self.messages.append({"role": "user", "parts": [prompt]})
        completion = self.model.generate_content(self.messages)
        self.messages.append(
            {
                "role": "model",
                "parts": [completion.text],
            }
        )
        logging.debug(f"Result from {self.get_name()}: {completion.text}")
        return App.model_validate_json(
            h.extract_json_from_markdown(completion.text), strict=False
        )
