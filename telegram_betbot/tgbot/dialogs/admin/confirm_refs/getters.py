from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.services.referral_service import ReferralService


async def admin_get_on_confirmed_refs(dialog_manager: DialogManager, **kwargs):
    bookmaker = dialog_manager.start_data.get("bet_company")
    bookmaker_id = dialog_manager.start_data["bookmaker_id"]
    streamer = dialog_manager.start_data.get("streamer")
    streamer_id = dialog_manager.start_data["streamer_id"]
    db = dialog_manager.middleware_data["db"]

    on_confirmed_refs = await ReferralService(db).get_referrals_by_where(
        bookmaker_id=bookmaker_id,
        streamer_id=streamer_id,
        is_confirmed=False,
    )

    on_confirmed_refs_dict: dict[int, int] = {
        ref.referral_key: ref.user_telegram_id for ref in on_confirmed_refs
    }

    dialog_manager.dialog_data["on_confirmed_refs"] = on_confirmed_refs_dict
    return {
        "bookmaker": bookmaker,
        "streamer": streamer,
        "on_confirmed_refs": "\n".join(map(str, on_confirmed_refs_dict.keys())),
    }
