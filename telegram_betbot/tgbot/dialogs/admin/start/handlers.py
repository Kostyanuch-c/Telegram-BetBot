from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from telegram_betbot.tgbot.services.referral_service import ReferralService
from telegram_betbot.tgbot.states.admin import (
    AdminChangeRefsLink,
    AdminConfirmRefs,
    AdminNewsletterSG,
)


async def admin_choice_bet_company(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    admin_choice = button.widget_id
    dialog_manager.dialog_data["bet_company"] = admin_choice
    await dialog_manager.next()


async def admin_choice_streamer(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    admin_choose_streamer = button.widget_id

    db = dialog_manager.middleware_data["db"]

    streamer_id, bookmaker_id = await ReferralService(db).get_dara_for_referral(
        bookmaker_name=dialog_manager.dialog_data["bet_company"],
        streamer_name=admin_choose_streamer,
    )

    new_start_data = {
        "bet_company": dialog_manager.dialog_data["bet_company"],
        "streamer": admin_choose_streamer,
        "streamer_id": streamer_id,
        "bookmaker_id": bookmaker_id,
    }

    start_data = dialog_manager.start_data
    if start_data.get("confirm_referrals"):
        await dialog_manager.start(data=new_start_data, state=AdminConfirmRefs.send_confirms)
    elif start_data.get("change_streamer_link"):
        await dialog_manager.start(data=new_start_data, state=AdminChangeRefsLink.send_link)
    else:
        await dialog_manager.start(data=new_start_data, state=AdminNewsletterSG.add_text_body_post)
