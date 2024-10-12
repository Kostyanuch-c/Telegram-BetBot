import re
from urllib.parse import urlparse

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button

from telegram_betbot.tgbot.exeptions.admin import ReferralKeyUniqueError
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.services.referral_service import ReferralService
from telegram_betbot.tgbot.services.streamer_bookmaker_service import StreamerBookmakerService


async def admin_choice_add_referal_or_work_with_link(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["add_referal"] = (
        True if button.widget_id == "add_referral_keys" else False
    )
    await dialog_manager.next()


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
    admin_choice = button.widget_id
    dialog_manager.dialog_data["streamer"] = admin_choice

    await dialog_manager.next()


async def admin_error_input_add_referral_or_link_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError,
):
    await message.answer(text=LEXICON_ADMIN['error_add_referral_or_link'])


async def admin_wrong_type_input_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    await message.answer(text=LEXICON_ADMIN['error_wrong_type_input'])


async def admin_correct_input_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str,
) -> None:
    db = dialog_manager.middleware_data["db"]
    bookmaker = dialog_manager.dialog_data["bet_company"]
    streamer = dialog_manager.dialog_data["streamer"]

    if dialog_manager.dialog_data.get("add_referal", False):
        referrals_keys = re.split(r"[\s]+", text.strip())
        try:
            await ReferralService(db).create_new_referral_keys(
                bookmaker_name=bookmaker,
                streamer_name=streamer,
                referral_keys=referrals_keys,
            )
            await dialog_manager.next()
        except ReferralKeyUniqueError as exception:
            await message.answer(exception.message)
    else:
        referral_link = urlparse(text)
        if all([referral_link.scheme, referral_link.netloc]):
            await StreamerBookmakerService(db).update_or_create_referral_link(
                bookmaker_name=bookmaker,
                streamer_name=streamer,
                referral_link=text,
            )
            await dialog_manager.next()
        else:
            await message.answer(LEXICON_ADMIN['error_is_not_url'])
