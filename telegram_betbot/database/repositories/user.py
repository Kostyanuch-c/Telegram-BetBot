"""User repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_betbot.database.models import User
from telegram_betbot.database.repositories.abstract import Repository
from telegram_betbot.tgbot.enums.role import Role


# def calculate_time_difference(telegram_date: int) -> float:
#     """Calculate time difference between user and Moscow."""
#
#     moscow_timezone = pytz.timezone('Europe/Moscow')
#     moscow_time = datetime.now(moscow_timezone)
#
#     time_diff = (moscow_time - telegram_date).total_seconds() / 3600
#     return time_diff


class UserRepo(Repository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def create_and_return(
        self,
        telegram_id: int,
        user_name: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        language_code: str | None = None,
        role: Role = Role.USER,
    ) -> User:
        user = User(
            telegram_id=telegram_id,  # type: ignore[call-arg]
            user_name=user_name,  # type: ignore[call-arg]
            first_name=first_name,  # type: ignore[call-arg]
            last_name=last_name,  # type: ignore[call-arg]
            language_code=language_code,  # type: ignore[call-arg]
            role=role,  # type: ignore[call-arg]
        )
        await self.session.merge(user)

        return user

    async def get_role(self, telegram_id: int) -> Role:
        """Get user role by id."""
        return await self.session.scalar(
            select(User.role).where(User.telegram_id == telegram_id).limit(1),
        )
