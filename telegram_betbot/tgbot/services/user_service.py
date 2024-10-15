from telegram_betbot.database import Database
from telegram_betbot.database.entities.user import UserEntity
from telegram_betbot.database.models import User
from telegram_betbot.tgbot.enums.role import Role


class UserService:
    def __init__(self, db: Database):
        self.db = db

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:
        async with self.db.user.session.begin():
            user: User = await self.db.user.get_by_where(
                User.telegram_id == telegram_id,
            )
            if user:
                return UserEntity(
                    id=user.id,
                    telegram_id=user.telegram_id,
                    user_name=user.user_name,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    role=user.role,
                )

    async def get_role_or_create_user(self, telegram_user_data: dict) -> int:
        user: UserEntity | None = await self.get_user_by_telegram_id(
            telegram_user_data["telegram_id"],
        )

        async with self.db.user.session.begin():
            if user is None:
                user: User = await self.db.user.create_and_return(**telegram_user_data)

            return user.role.value

    async def update_user_role(self, telegram_id: int, role: Role) -> None:
        async with self.db.user.session.begin():
            await self.db.user.update_user_role(telegram_id, role)
