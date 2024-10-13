import re

from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from telegram_betbot.tgbot.exeptions.admin import ReferralUpdateStatusError
from telegram_betbot.tgbot.services.referral_service import ReferralService


async def admin_correct_input_confirmed_refs_id_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
) -> None:
    db = dialog_manager.middleware_data["db"]
    bookmaker_id = dialog_manager.start_data["bookmaker_id"]
    streamer_id = dialog_manager.start_data["streamer_id"]

    referrals_keys = re.split(r"[\s]+", text.strip())
    try:
        await ReferralService(db).update_referral_status(
            bookmaker_id=bookmaker_id,
            streamer_id=streamer_id,
            referral_keys=referrals_keys,
        )
        await dialog_manager.next()
    except ReferralUpdateStatusError as exception:
        await message.answer(exception.message)
