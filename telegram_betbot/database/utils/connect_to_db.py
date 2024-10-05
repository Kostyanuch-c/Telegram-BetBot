import logging

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine as _create_async_engine,
)


logger = logging.getLogger(__name__)


def create_async_engine(url: URL | str, echo: bool = False) -> AsyncEngine:
    """Create async engine with given URL.

    :param echo:
    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=echo, pool_pre_ping=True)
