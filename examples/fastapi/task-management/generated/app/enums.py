import enum


class Status(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
