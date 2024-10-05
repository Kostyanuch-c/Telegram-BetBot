from aiogram.types import User

from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.lexicon.lexicon import BOOKMAKER_LINKS, LEXICON_RU


async def get_start_message(
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    username = event_from_user.full_name or event_from_user.username or LEXICON_RU["default_name"]
    return {"username": username}


async def get_registration_link(dialog_manager: DialogManager, **kwargs):
    bet_company = dialog_manager.dialog_data.get("bet_company")
    streamer = dialog_manager.dialog_data.get("streamer")

    link = BOOKMAKER_LINKS[bet_company][streamer]

    return {
        "registration_link": link,
        "streamer": f"{streamer} {bet_company}",
    }
