from telegram_betbot.database import Database
from telegram_betbot.database.models import User


class UserService:
    def __init__(self, db: Database):
        self.db = db

    async def register_user(self, telegram_user_data: dict) -> None:
        async with self.db.session.begin():
            user: User = await self.db.user.get_by_where(
                User.telegram_id == telegram_user_data['telegram_id'],
            )

            if user is None:
                await self.db.user.new(**telegram_user_data)
