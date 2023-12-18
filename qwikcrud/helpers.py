import contextlib
import os
import re
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


def extract_json_from_markdown(markdown_text):
    # Regular expression to find a JSON object in the text
    json_pattern = re.compile(r"```(json)?(.*)```", re.DOTALL)

    # Attempt to find a JSON object in the text
    json_match = json_pattern.search(markdown_text)

    if json_match:
        # If match found, extract the JSON string from the code block
        json_str = json_match.group(2)
    else:
        # If no JSON object is found, consider the entire text as JSON
        json_str = markdown_text
    return json_str


def apply_python_naming_convention(app: "App"):
    for entity in app.entities:
        for field in entity.fields:
            field.name = snake_case(field.name)
    for relation in app.relations:
        relation.field_name = snake_case(relation.field_name)
        relation.backref_field_name = snake_case(relation.backref_field_name)
