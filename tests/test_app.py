from pathlib import Path

from qwikcrud.schemas import App


def test_validate():
    with open(Path(__file__).parent / "dummy.json") as f:
        App.model_validate_json(f.read())
