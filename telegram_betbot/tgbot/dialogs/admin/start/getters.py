from aiogram.types import User

from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU


async def admin_get_start_message(
    event_from_user: User,
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    username = event_from_user.full_name or event_from_user.username or LEXICON_RU["default_name"]

    return {
        "username": username,
    }
