from qwikcrud import helpers as h
from qwikcrud.schemas import App


def test_validate():
    App.model_validate_json(open(h.path_to("tests/app.json")).read())
