import contextlib
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qwikcrud.schemas import App


def path_to(relative: str):
    return Path(__file__).parent / relative


def make_dirs(_dir: Path):
    os.makedirs(_dir, 0o777, exist_ok=True)


def delete_dir(_dir: Path):
    shutil.rmtree(_dir, ignore_errors=True)


def delete_file(file: Path):
    with contextlib.suppress(FileNotFoundError):
        os.remove(file)


def lower_first_character(text: str) -> str:
    return text[0].lower() + text[1:]


def upper_first_character(text: str) -> str:
    return text[0].upper() + text[1:]


def snake_case(text: str) -> str:
    return "".join(["_" + c.lower() if c.isupper() else c for c in text]).lstrip("_")


def apply_python_naming_convention(app: "App"):
    for entity in app.entities:
        for field in entity.fields:
            field.name = snake_case(field.name)
    for relation in app.relations:
        relation.field_name = snake_case(relation.field_name)
        relation.backref_field_name = snake_case(relation.backref_field_name)
