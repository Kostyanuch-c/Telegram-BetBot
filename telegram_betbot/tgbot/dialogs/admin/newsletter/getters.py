from aiogram.types import User

from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN, LEXICON_RU


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
        "work_with_link": LEXICON_ADMIN["add_link"],
        "work_with_photo": LEXICON_ADMIN["add_photo"],
        "streamer": dialog_manager.start_data["streamer"],
        "bookmaker": dialog_manager.start_data["bet_company"],
    }

    if dialog_manager.dialog_data["newsletter"].get("photo"):
        response_dict["work_with_photo"] = LEXICON_ADMIN["change_photo"]
    if dialog_manager.dialog_data["newsletter"].get("keyboard_data"):
        response_dict["work_with_link"] = LEXICON_ADMIN["change_link"]
    return response_dict


async def get_result_newsletter_message(
    event_from_user: User,
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    successfully_sent = dialog_manager.dialog_data["newsletter"].get("successfully_sent")
    total_messages = dialog_manager.dialog_data["newsletter"].get("total_messages")
    return {
        "successfully_sent": successfully_sent,
        "total_messages": total_messages,
    }
