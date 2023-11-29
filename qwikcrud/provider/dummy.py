import time

from qwikcrud.helpers import path_to
from qwikcrud.provider.base import AIProvider
from qwikcrud.schemas import App


class DummyAIProvider(AIProvider):
    def get_name(self) -> str:
        return "DummyAI"

    def query(self, prompt: str) -> App:  # noqa ARG002
        time.sleep(0.1)
        return App.model_validate_json(open(path_to("examples/app.json")).read())
