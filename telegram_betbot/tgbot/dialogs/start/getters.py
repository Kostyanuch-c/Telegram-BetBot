from aiogram.types import User

from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU
from telegram_betbot.tgbot.services.streamer_bookmaker_service import StreamerBookmakerService


CHANNELS_LINKS = {
    "Pari": {
        "streamer_1": "https://t.me/+eBjbMt7nsjsxZDEy",
        "streamer_2": "https://t.me/+eBjbMt7nsjsxZDEy",
        "streamer_3": "https://t.me/+eBjbMt7nsjsxZDEy",
    },
    "Upx": {
        "streamer_1": "https://t.me/+eBjbMt7nsjsxZDEy",
        "streamer_2": "https://t.me/+eBjbMt7nsjsxZDEy",
        "streamer_3": "https://t.me/+eBjbMt7nsjsxZDEy",
    },
}


async def get_start_message(
        event_from_user: User,
        dialog_manager: DialogManager,
        **kwargs,
) -> dict[str, str]:
    username = event_from_user.full_name or event_from_user.username or LEXICON_RU["default_name"]

    if not dialog_manager.dialog_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)

    occupied_bookmakers = dialog_manager.dialog_data.get("occupied_bookmakers", {})
    streamer_pari = occupied_bookmakers.get("Pari", False)
    streamer_upx = occupied_bookmakers.get("Upx", False)

    response_data = {
        "username": username,
        "all_free": True,
        "only_pari": False,
        "only_upx": False,
        "all_bm": False,
    }

    if streamer_pari:
        response_data.update({
            "streamer_pari": streamer_pari,
            "pari_link": CHANNELS_LINKS["Pari"][streamer_pari],
            "only_pari": True,
            "all_free": False,
        })

    if streamer_upx:
        response_data.update({
            "streamer_upx": streamer_upx,
            "upx_link": CHANNELS_LINKS["Upx"][streamer_upx],
            "all_free": False,
            "only_upx": not streamer_pari,
            "only_pari": False,
            "all_bm": bool(streamer_pari),
        })

    response_data["one_or_more_free"] = not (streamer_pari and streamer_upx)
    return response_data


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


async def get_streamer_chanel_link(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    bet_company = dialog_manager.dialog_data.get("bet_company")
    streamer = dialog_manager.dialog_data.get("streamer")

    return {"channel_link": CHANNELS_LINKS[bet_company][streamer]}


async def get_bookmaker_name(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    bet_company = dialog_manager.dialog_data.get("bet_company")
    return {"bookmaker": bet_company}
