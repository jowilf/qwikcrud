from typing import Annotated, Generator

from app.db import Session
from fastapi import Depends


def get_db() -> Generator:
    with Session() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
