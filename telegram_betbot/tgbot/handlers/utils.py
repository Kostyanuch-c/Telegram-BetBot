from aiogram.types import User

from aiogram_dialog import DialogManager

from telegram_betbot.database import Database
from telegram_betbot.tgbot.services.referral_service import ReferralService


def extract_user_data(telegram_user: User) -> dict[str, any]:
    return {
        "telegram_id": telegram_user.id,
        "first_name": telegram_user.first_name,
        "last_name": telegram_user.last_name,
        "language_code": telegram_user.language_code,
        "user_name": telegram_user.username,
    }


async def check_free_bookmakers(
    db: Database,
    user: User,
    dialog_manager: DialogManager,
):
    occupied_bookmakers, free_bookmakers = await ReferralService(db).check_free_bookmakers(
        telegram_id=user.id,
    )

    return occupied_bookmakers, free_bookmakers
