"""User repository file."""
from typing import cast

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_betbot.database.models import User
from telegram_betbot.database.repositories.abstract import Repository
from telegram_betbot.tgbot.enums.role import Role


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

        self.session.add(user)
        return user

    async def update_user_role(
        self,
        telegram_id: int,
        role: Role,
    ) -> None:
        query = (
            update(User)
            .where(cast("ColumnElement[bool]", User.telegram_id == telegram_id))
            .values(role=role)
        )
        await self.session.execute(query)
