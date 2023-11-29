import logging

from qwikcrud.settings import settings


def setup_logging():
    logging.basicConfig(
        format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=settings.logging_level,
    )
