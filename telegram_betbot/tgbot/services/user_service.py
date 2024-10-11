from telegram_betbot.database import Database
from telegram_betbot.database.models import User


class UserService:
    def __init__(self, db: Database):
        self.db = db

    async def get_role_or_create_user(self, telegram_user_data: dict) -> int:
        async with self.db.user.session.begin():
            user: User = await self.db.user.get_by_where(
                User.telegram_id == telegram_user_data["telegram_id"],
            )

            if user is None:
                user: User = await self.db.user.create_and_return(**telegram_user_data)

            return user.role.value
