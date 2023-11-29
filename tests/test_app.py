from pathlib import Path

from qwikcrud.schemas import App


def test_validate():
    App.model_validate_json(open(Path(__file__).parent / "app.json").read())
