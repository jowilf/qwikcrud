from abc import abstractmethod
from pathlib import Path

import autoflake
import black
import isort
from jinja2 import Environment, FileSystemLoader

from qwikcrud import helpers as h
from qwikcrud.schemas import App


class BaseAppGenerator:
    def __init__(self, output_directory: Path) -> None:
        self.env = Environment(  # noqa: S701
            loader=FileSystemLoader(h.path_to("templates")),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["snake_case"] = h.snake_case
        self.output_directory = output_directory

    def _write_code_into_file(self, path, code_text: str, format_code: bool = True):
        with open(self.output_directory / f"{path}", "w") as file:
            if format_code:
                code_text = black.format_str(code_text, mode=black.Mode())
                code_text = autoflake.fix_code(
                    code_text, remove_all_unused_imports=True
                )
                code_text = isort.code(code_text)
            file.write(code_text)

    def _generate_from_template(
        self,
        app: App,
        relative_template_path,
        destination_path=None,
        template_data=None,
        skip_render=False,
        extension="py",
    ):
        if template_data is None:
            template_data = {"app": app}
        if destination_path is None:
            destination_path = relative_template_path
        if skip_render:
            template_text = open(
                f"{h.path_to('templates')}/{self._absolute_template_path(f'{relative_template_path}.{extension}')}"
            ).read()
            self._write_code_into_file(
                f"{destination_path}.{extension}", template_text, extension == "py"
            )
        else:
            template = self.env.get_template(
                self._absolute_template_path(f"{relative_template_path}.{extension}.j2")
            )
            rendered_code = template.render(template_data)
            self._write_code_into_file(
                f"{destination_path}.{extension}", rendered_code, extension == "py"
            )

    @abstractmethod
    def _absolute_template_path(self, relative_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(self, app: App) -> None:
        raise NotImplementedError

    @abstractmethod
    def clean(self):
        raise NotImplementedError


class FastAPIAppGenerator(BaseAppGenerator):
    def _absolute_template_path(self, relative_path: str) -> str:
        return f"fastapi/{relative_path}"

    def generate(self, app: App) -> None:
        h.apply_python_naming_convention(app)
        h.make_dirs(self.output_directory / "app")
        h.make_dirs(self.output_directory / "templates")
        h.make_dirs(self.output_directory / "static/css")
        self._generate_from_template(app, "app/__init__")
        self._generate_from_template(app, "app/models")
        self._generate_from_template(app, "app/schemas")
        self._generate_from_template(app, "app/crud")
        self._generate_from_template(app, "app/deps")
        self._generate_from_template(app, "app/settings")
        self._generate_from_template(app, "app/db")
        self._generate_from_template(app, "app/pre_start")
        self._generate_from_template(app, "app/main")
        self._generate_from_template(app, "app/admin")
        self._generate_from_template(app, "requirements", extension="txt")
        self._generate_from_template(app, "README", extension="md")
        self._generate_from_template(
            app, "templates/index", extension="html", skip_render=True
        )
        self._generate_from_template(
            app, "static/css/style", extension="css", skip_render=True
        )
        self.__generate_endpoints(app)
        if app.has_file():
            self._generate_from_template(app, "app/storage")
        if app.has_enum():
            self._generate_from_template(app, "app/enums")
        self._write_code_into_file(
            ".qwikcrud.json.lock", app.model_dump_json(indent=4), format_code=False
        )

    def __generate_endpoints(self, app: App) -> None:
        h.make_dirs(self.output_directory / "app/endpoints")
        self._generate_from_template(app, "app/endpoints/__init__")
        for entity in app.entities:
            template_path = "app/endpoints/template"
            destination_path = f"app/endpoints/{entity.name.lower()}"
            self._generate_from_template(
                app, template_path, destination_path, {"entity": entity, "app": app}
            )

    def clean(self):
        h.delete_dir(self.output_directory / "app")
        h.delete_dir(self.output_directory / "templates")
        h.delete_dir(self.output_directory / "static")
        h.delete_file(self.output_directory / "requirements.txt")
        h.delete_file(self.output_directory / "README.md")
