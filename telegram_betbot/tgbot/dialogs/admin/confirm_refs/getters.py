from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.services.referral_service import ReferralService


async def admin_get_not_confirmed_refs(dialog_manager: DialogManager, **kwargs):
    bookmaker = dialog_manager.start_data.get("bet_company")
    bookmaker_id = dialog_manager.start_data["bookmaker_id"]
    streamer = dialog_manager.start_data.get("streamer")
    streamer_id = dialog_manager.start_data["streamer_id"]
    db = dialog_manager.middleware_data["db"]

    not_confirmed_refs = await ReferralService(db).get_referrals_id_by_bm_and_streamer(
        bookmaker_id=bookmaker_id,
        streamer_id=streamer_id,
    )

    return {
        "bookmaker": bookmaker,
        "streamer": streamer,
        "not_confirmed_refs": "\n".join(map(str, not_confirmed_refs)),
    }
