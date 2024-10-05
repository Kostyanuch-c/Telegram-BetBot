"""User repository file."""

from datetime import datetime

import pytz
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_betbot.database.models import User
from telegram_betbot.database.repositories.abstract import Repository
from telegram_betbot.tgbot.enums.role import Role


def calculate_time_difference(telegram_date: int) -> float:
    """Calculate time difference between user and Moscow."""

    moscow_timezone = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_timezone)

    time_diff = (moscow_time - telegram_date).total_seconds() / 3600
    return time_diff


class UserRepo(Repository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def new(
            self,
            telegram_id: int,
            telegram_date: int,
            user_name: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            language_code: str | None = None,
            is_premium: bool | None = False,
            role: Role = Role.USER,

    ) -> None:
        time_difference_moscow = calculate_time_difference(telegram_date)

        await self.session.merge(
            User(
                telegram_id=telegram_id,
                user_name=user_name,
                first_name=first_name,
                last_name=last_name,
                language_code=language_code,
                role=role,
                time_difference_moscow=time_difference_moscow,
            ),
        )

        await self.session.commit()

    async def get_role(self, telegram_id: int) -> Role:
        """Get user role by id."""
        return await self.session.scalar(
            select(User.role).where(User.telegram_id == telegram_id).limit(1),
        )
