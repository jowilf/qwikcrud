from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field, model_validator
from rich.console import Console
from rich.tree import Tree

from qwikcrud import helpers as h


class FieldType(str, Enum):
    ID = "ID"
    Integer = "Integer"
    Float = "Float"
    Boolean = "Boolean"
    Date = "Date"
    Time = "Time"
    DateTime = "DateTime"
    String = "String"
    Text = "Text"
    Enum = "Enum"
    Email = "Email"
    JSON = "JSON"
    Image = "Image"
    File = "File"

    @classmethod
    def _missing_(cls: "FieldType", value: str) -> Optional["str"]:
        """When an invalid or case-mismatched string value is provided, this method attempts to find a
        case-insensitive match among the enum members."""
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


field_python_type_mapping = {
    FieldType.ID: "int",
    FieldType.Integer: "int",
    FieldType.Float: "float",
    FieldType.Boolean: "bool",
    FieldType.Date: "datetime.date",
    FieldType.Time: "datetime.time",
    FieldType.DateTime: "datetime.datetime",
    FieldType.String: "str",
    FieldType.Text: "str",
    FieldType.Enum: "str",
    FieldType.Email: "EmailStr",
    FieldType.JSON: "dict",
    FieldType.Image: "Union[File, UploadFile, None]",
    FieldType.File: "Union[File, UploadFile, None]",
}


class RelationType(str, Enum):
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_MANY = "MANY_TO_MANY"

    @classmethod
    def _missing_(cls: "FieldType", value: str) -> Optional["str"]:
        """When an invalid or case-mismatched string value is provided, this method attempts to find a
        case-insensitive match among the enum members."""
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class Constraints(BaseModel):
    unique: Optional[bool] = Field(None)
    not_null: Optional[bool] = Field(None)
    gt: Optional[float] = Field(None)
    ge: Optional[float] = Field(None)
    lt: Optional[float] = Field(None)
    le: Optional[float] = Field(None)
    multiple_of: Optional[float] = Field(None)
    min_length: Optional[int] = Field(None)
    max_length: Optional[int] = Field(None)
    mime_types: Optional[List[str]] = Field(None)
    allowed_values: Optional[List[str]] = Field(None)

    def get_allowed_values(self):
        return self.allowed_values or []


class FieldModel(BaseModel):
    name: str = Field(...)
    type_: FieldType = Field(..., alias="type")
    constraints: Optional[Constraints] = Field(Constraints())

    @model_validator(mode="after")
    def root_validator(self) -> "FieldModel":
        self.name = h.lower_first_character(self.name)
        return self

    def is_id(self):
        return self.type_ == FieldType.ID

    def is_file(self):
        return self.type_ in (FieldType.Image, FieldType.File)

    def sqla_column_def(self) -> str:
        """Generate the sqlalchemy column definition

        Example:
            id: Mapped[int] = mapped_column(primary_key=True)
        """
        type_mapping = field_python_type_mapping.get(self.type_)
        if self.constraints.not_null:
            type_mapping = f"Optional[{type_mapping}]"
        mapped_column_kwargs = []
        if self.type_ in [FieldType.Image, FieldType.File]:
            file_field_mapping = (
                "ImageField" if self.type_ == FieldType.Image else "FileField"
            )
            file_field_mapping_kwargs = []
            if self.type_ == FieldType.Image:
                file_field_mapping_kwargs.append("thumbnail_size=(150,150)")
            file_field_validators = ['SizeValidator(max_size="20M")']
            if self.constraints.mime_types:
                mimetypes_list = ",".join(
                    ('"' + v + '"') for v in self.constraints.mime_types
                )
                file_field_validators.append(
                    f"ContentTypeValidator([{mimetypes_list}])"
                )
            file_field_mapping_kwargs.append(
                f'validators=[{",".join(file_field_validators)}]'
            )
            file_field_mapping += f'({",".join(file_field_mapping_kwargs)})'
            mapped_column_kwargs.append(file_field_mapping)
        if self.type_ == FieldType.Enum:
            mapped_column_kwargs.append(f"Enum({self.name.capitalize()})")
        if self.constraints.unique:
            mapped_column_kwargs.append("unique=True")
        if self.type_ == FieldType.ID:
            mapped_column_kwargs.append("primary_key=True")
        return f"{h.snake_case(self.name)}: Mapped[{type_mapping}]" + (
            f'=mapped_column({",".join(mapped_column_kwargs)})'
            if len(mapped_column_kwargs) > 0
            else ""
        )

    def pydantic_def(self, all_optional: bool = False):
        type_mapping = field_python_type_mapping.get(self.type_)
        if self.type_ == FieldType.Enum:
            type_mapping = self.name.capitalize()
        if all_optional or self.constraints.not_null:
            type_mapping = f"Optional[{type_mapping}]"
        if self.is_file():
            type_mapping = "Optional[FileInfo]"
        pydantic_field_kwargs = [
            f"{k}={v}"
            for (k, v) in self.constraints.model_dump(
                exclude={"unique", "not_null", "allowed_values"}, exclude_none=True
            ).items()
        ]
        if all_optional:
            pydantic_field_kwargs = ["None", *pydantic_field_kwargs]

        return f"{h.snake_case(self.name)}: {type_mapping}" + (
            f'=Field({",".join(pydantic_field_kwargs)})'
            if len(pydantic_field_kwargs) > 0
            else ""
        )


class Entity(BaseModel):
    name: str = Field(...)
    fields: List[FieldModel] = Field(...)

    @model_validator(mode="after")
    def root_validator(self) -> "Entity":
        self.name = h.upper_first_character(self.name)
        return self


class Relation(BaseModel):
    name: str
    type_: RelationType = Field(..., alias="type")
    from_: str = Field(..., alias="from")
    to: str
    field_name: str
    backref_field_name: str

    @model_validator(mode="after")
    def root_validator_mode_after(self) -> "Relation":
        self.name = h.upper_first_character(self.name)
        self.from_ = h.upper_first_character(self.from_)
        self.to = h.upper_first_character(self.to)
        self.field_name = h.lower_first_character(self.field_name)
        self.backref_field_name = h.lower_first_character(self.backref_field_name)
        return self

    @model_validator(mode="before")
    @classmethod
    def root_validator_mode_before(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Transform MANY_TO_ONE to ONE_TO_MANY
            if data.get("type", "ONE_TO_ONE").upper() == "MANY_TO_ONE":
                data["type"] = "ONE_TO_MANY"
                data["from"], data["to"] = data["to"], data["from"]
                data["field_name"], data["backref_field_name"] = (
                    data["backref_field_name"],
                    data["field_name"],
                )
        return data


class App(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    entities: List[Entity] = Field(...)
    relations: List[Relation] = Field(...)

    def has_file(self) -> bool:
        for entity in self.entities:
            for field in entity.fields:
                if field.is_file():
                    return True
        return False

    def has_enum(self) -> bool:
        for entity in self.entities:
            for field in entity.fields:
                if field.type_ == FieldType.Enum:
                    return True
        return False

    def summary(self):
        console = Console()
        console.print(f"[bold magenta]Name[/bold magenta]: {self.name}")
        console.print(f"[bold magenta]Description[/bold magenta]: {self.description}")
        console.print("\n[bold underline]Entities:[/bold underline]\n")

        for entity in self.entities:
            entity_tree = Tree(f"[bold cyan]{entity.name}[/bold cyan]")
            for field in entity.fields:
                field_str = f"[cyan]{field.name}[/cyan]: [yellow]{field.type_}[/yellow]"
                constraints_str = ", ".join(
                    f"{key}={value}"
                    for key, value in field.constraints.model_dump().items()
                    if value is not None
                )
                if constraints_str:
                    field_str += f" ({constraints_str})"
                entity_tree.add(field_str)

            console.print(entity_tree)
            console.print("\n")

        if self.relations:
            console.print("[bold underline]Relationships:[/bold underline]\n")

            for relation in self.relations:
                console.print(
                    f"[bold cyan]{relation.from_}[/bold cyan] ([magenta]{relation.field_name}[/magenta])"
                    f" --[{relation.type_}]--> [bold cyan]{relation.to}[/bold cyan]"
                    f" ([magenta]{relation.backref_field_name}[/magenta])"
                )
            console.print("\n")
