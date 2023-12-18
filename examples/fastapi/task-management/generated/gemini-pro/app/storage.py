from libcloud.storage.base import Container, StorageDriver
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ContainerDoesNotExistError
from sqlalchemy_file.storage import StorageManager


def get_or_create_container(driver: StorageDriver, name: str) -> Container:
    try:
        return driver.get_container(name)
    except ContainerDoesNotExistError:
        return driver.create_container(name)


async def init_storage() -> None:
    StorageManager.add_storage(
        "default", get_or_create_container(LocalStorageDriver("."), "assets")
    )
