from aiogram.types import User

from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU
from telegram_betbot.tgbot.services.streamer_bookmaker_service import StreamerBookmakerService


async def get_start_message(
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    username = event_from_user.full_name or event_from_user.username or LEXICON_RU["default_name"]
    return {"username": username}


async def get_registration_link(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    bet_company = dialog_manager.dialog_data.get("bet_company")
    streamer = dialog_manager.dialog_data.get("streamer")
    db = dialog_manager.middleware_data["db"]

    referral_link = await StreamerBookmakerService(db).get_referral_link(
        bookmaker_name=bet_company,
        streamer_name=streamer,
    )

    return {
        "registration_link": referral_link,
        "streamer": f"{streamer} {bet_company}",
    }
