
from app.db import init_db
from app.storage import init_storage


async def init() -> None:
    await init_db()
    await init_storage()
