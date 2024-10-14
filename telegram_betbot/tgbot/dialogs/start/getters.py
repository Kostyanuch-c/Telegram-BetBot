from aiogram.types import User

from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.dialogs.start.start_message import create_start_message
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU
from telegram_betbot.tgbot.services.streamer_bookmaker_service import StreamerBookmakerService


async def get_start_message(
    event_from_user: User,
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    username = event_from_user.full_name or event_from_user.username or LEXICON_RU["default_name"]

    if not dialog_manager.dialog_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)

    occupied_bookmakers = dialog_manager.dialog_data.get("occupied_bookmakers", {})
    streamer_pari: list[str, bool] | bool = occupied_bookmakers.get("Pari", False)
    streamer_upx: list[str, bool] | bool = occupied_bookmakers.get("Upx", False)

    response_data: dict = {
        "username": username,
        "status_pari": streamer_pari[1] if streamer_pari else "not_attempted",
        "status_upx": streamer_upx[1] if streamer_upx else "not_attempted",
        "one_or_more_not_free": False,
    }

    response_data = create_start_message(response_data, streamer_pari, streamer_upx)
    return response_data


async def get_registration_link(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    bet_company = dialog_manager.dialog_data.get("bet_company")
    streamer = dialog_manager.dialog_data.get("streamer")

    bookmaker_id = dialog_manager.dialog_data["bookmaker_id"]
    steamer_id = dialog_manager.dialog_data["streamer_id"]
    db = dialog_manager.middleware_data["db"]

    referral_link = await StreamerBookmakerService(db).get_referral_link(
        bookmaker_id=bookmaker_id,
        streamer_id=steamer_id,
    )

    return {
        "registration_link": referral_link,
        "streamer": f"{streamer} {bet_company}",
    }


async def get_bookmaker_name(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    bet_company = dialog_manager.dialog_data.get("bet_company")
    return {"bookmaker": bet_company}
