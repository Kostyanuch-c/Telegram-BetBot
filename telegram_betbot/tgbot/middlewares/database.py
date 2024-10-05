import logging
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_betbot.database import Database


logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler."""

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[None]],
        event: Message | CallbackQuery,
        data: dict[str, any],
    ) -> any:
        """This method calls every update."""
        async with AsyncSession(bind=data["db_engine"]) as session:
            data["db"] = Database(session)
            return await handler(event, data)
