from aiogram.types import User

from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)

from telegram_betbot.database import Database
from telegram_betbot.tgbot.services.referral_service import ReferralService
from telegram_betbot.tgbot.states.start import StartSG


def extract_user_data(telegram_user: User) -> dict[str, any]:
    return {
        "telegram_id": telegram_user.id,
        "first_name": telegram_user.first_name,
        "last_name": telegram_user.last_name,
        "language_code": telegram_user.language_code,
        "user_name": telegram_user.username,
    }


async def to_start_dialog(
    db: Database,
    user: User,
    dialog_manager: DialogManager,
    show_mode: ShowMode = ShowMode.AUTO,
):
    occupied_bookmakers, free_bookmakers = await ReferralService(db).check_free_bookmakers(
        telegram_id=user.id,
    )
    await dialog_manager.start(
        state=StartSG.start,
        mode=StartMode.RESET_STACK,
        show_mode=show_mode,
        data={
            "occupied_bookmakers": occupied_bookmakers,
            "free_bookmakers": free_bookmakers,
        },
    )
