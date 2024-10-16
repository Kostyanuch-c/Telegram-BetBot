import asyncio

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button

from telegram_betbot.tgbot.dialogs.admin.newsletter.newsletter import (
    send_message_to_user,
    send_newsletter_message_to_admin_for_check,
)
from telegram_betbot.tgbot.keyboards.url import create_keyboard_from_data
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN_ERRORS
from telegram_betbot.tgbot.services.referral_service import ReferralService
from telegram_betbot.tgbot.states.admin import AdminNewsletterSG


async def admin_button_clear_data_post(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data.get("newsletter", {}).clear()
    await dialog_manager.done()


async def admin_correct_input_body_post_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
) -> None:
    newsletter_data = dialog_manager.dialog_data.get("newsletter", {})
    newsletter_data["text"] = text

    dialog_manager.dialog_data["newsletter"] = newsletter_data

    changing_mod = newsletter_data.get("changing_mod")
    if changing_mod:
        await send_newsletter_message_to_admin_for_check(
            newsletter_data=newsletter_data,
            dialog_manager=dialog_manager,
            admin_chat_id=message.chat.id,
        )
        await dialog_manager.switch_to(state=AdminNewsletterSG.check_newsletter)
    else:
        await dialog_manager.next()


async def admin_wrong_type_input_photo_for_newsletter_handler(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    await message.answer(text=LEXICON_ADMIN_ERRORS["error_inout_type_photo"])


async def admin_choice_post_without_photo(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.next()


async def admin_correct_input_photo_for_newsletter_handler(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["newsletter"]["photo"] = message.photo[1].file_id
    newsletter_data = dialog_manager.dialog_data.get("newsletter")

    changing_mod = newsletter_data.get("changing_mod")
    if changing_mod:
        await send_newsletter_message_to_admin_for_check(
            newsletter_data=newsletter_data,
            dialog_manager=dialog_manager,
            admin_chat_id=message.chat.id,
        )
        await dialog_manager.switch_to(state=AdminNewsletterSG.check_newsletter)
    else:
        await dialog_manager.next()


async def admin_choice_post_without_url_button(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    """Can't check this handler with changing_mod=True"""
    newsletter_data = dialog_manager.dialog_data["newsletter"]
    text = newsletter_data.get("text")
    photo = newsletter_data.get("photo")

    dialog_manager.dialog_data["newsletter"]["changing_mod"] = True

    bot: Bot = dialog_manager.middleware_data["bot"]
    dialog_manager.show_mode = ShowMode.SEND
    if photo:
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=photo,
            caption=text,
        )
        await dialog_manager.switch_to(state=AdminNewsletterSG.check_newsletter)
    else:
        await callback.bot.send_message(chat_id=callback.message.chat.id, text=text)

        await dialog_manager.next()


async def admin_correct_input_url_newsletter_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
):
    dialog_manager.dialog_data["newsletter"]["changing_mod"] = True

    button_text, url = text.strip().split("\n")

    dialog_manager.dialog_data["newsletter"]["keyboard_data"] = {
        "url": url,
        "text": button_text,
    }

    newsletter_data = dialog_manager.dialog_data["newsletter"]

    await send_newsletter_message_to_admin_for_check(
        newsletter_data=newsletter_data,
        dialog_manager=dialog_manager,
        admin_chat_id=message.chat.id,
    )

    await dialog_manager.next()


async def admin_send_newsletter(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    db = dialog_manager.middleware_data["db"]
    bot: Bot = dialog_manager.middleware_data["bot"]

    newsletter_data = dialog_manager.dialog_data["newsletter"]
    photo = newsletter_data.get("photo")
    text = newsletter_data.get("text")

    keyboard_data = newsletter_data.get("keyboard_data", {})
    keyboard = create_keyboard_from_data(keyboard_data)

    streamer_id = dialog_manager.start_data["streamer_id"]
    bookmaker_id = dialog_manager.start_data["bookmaker_id"]

    refs = await ReferralService(db).get_referrals_by_where(
        streamer_id=streamer_id,
        bookmaker_id=bookmaker_id,
        is_confirmed=True,
    )
    total_messages = len(refs)
    successfully_sent = 0
    await callback.message.answer(
        text=f"Отправляю {total_messages} сообщений, пожалуйста, подождите",
    )

    for ref in refs:
        success = await send_message_to_user(
            ref_id=ref.user_telegram_id,
            message=text,
            bot=bot,
            photo=photo,
            keyboard=keyboard,
        )
        if success:
            successfully_sent += 1
        await asyncio.sleep(0.1)

    dialog_manager.dialog_data["newsletter"].update(
        {
            "successfully_sent": successfully_sent,
            "total_messages": total_messages,
        },
    )

    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.next()
