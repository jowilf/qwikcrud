import contextlib
import os
import shutil
from pathlib import Path


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
