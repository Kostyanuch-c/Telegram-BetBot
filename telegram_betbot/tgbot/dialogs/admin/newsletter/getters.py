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


async def get_data_check_newsletter_message(
    event_from_user: User,
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    response_dict: dict[str, str] = {
        "work_with_photo": "Добавить фото",
        "streamer": dialog_manager.dialog_data.get("streamer"),
        "bookmaker": dialog_manager.dialog_data.get("bet_company"),
    }

    if dialog_manager.dialog_data["newsletter"].get("photo"):
        response_dict["work_with_photo"] = "Изменить фото"
    return response_dict
