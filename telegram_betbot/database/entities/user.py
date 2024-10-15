from dataclasses import dataclass

from telegram_betbot.tgbot.enums.role import Role


@dataclass
class UserEntity:
    id: int  # noqa
    telegram_id: int
    user_name: str | None
    first_name: str | None
    last_name: str | None
    role: Role
