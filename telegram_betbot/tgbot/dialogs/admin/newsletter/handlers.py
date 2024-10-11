import asyncio
import logging
from pprint import pprint

from aiogram import Bot
from aiogram.exceptions import (
    DetailedAiogramError,
    TelegramForbiddenError,
    TelegramRetryAfter,
)
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button

from telegram_betbot.tgbot.services.referral_service import ReferralService
from telegram_betbot.tgbot.states.admin import AdminNewsletterSG


logger = logging.getLogger(__name__)


async def admin_button_clear_data_post(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data.get("newsletter", {}).clear()
    await dialog_manager.back()


async def admin_correct_input_body_post(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
) -> None:
    newsletter_data = dialog_manager.dialog_data.get("newsletter", {})

    newsletter_data["text"] = text
    photo = newsletter_data.get("photo")

    dialog_manager.dialog_data["newsletter"] = newsletter_data
    bot: Bot = dialog_manager.middleware_data["bot"]

    if photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=text,
        )
        await dialog_manager.switch_to(state=AdminNewsletterSG.check_newsletter)
    else:
        await dialog_manager.next()


async def admin_wrong_type_input_photo_for_newsletter(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    await message.answer(text="Отправте, пожалуйста, фото!")


async def admin_choice_post_without_photo(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    newsletter_data = dialog_manager.dialog_data["newsletter"]
    text = newsletter_data.get("text")

    await callback.bot.send_message(chat_id=callback.message.chat.id, text=text)

    await dialog_manager.next()


async def admin_correct_input_photo_for_newsletter(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["newsletter"]["photo"] = message.photo[1].file_id
    pprint(dialog_manager.dialog_data)
    newsletter_data = dialog_manager.dialog_data["newsletter"]
    photo = newsletter_data.get("photo")
    text = newsletter_data.get("text")

    bot: Bot = dialog_manager.middleware_data["bot"]

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=text,
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

    streamer_name = dialog_manager.dialog_data.get("streamer")
    bookmaker_name = dialog_manager.dialog_data.get("bet_company")

    refs_ids = await ReferralService(db).get_referrals_by_bm_and_streamer(
        streamer_name=streamer_name,
        bookmaker_name=bookmaker_name,
    )
    total_messages = len(refs_ids)
    successfully_sent = 0
    await callback.message.answer(
        text=f"Отправляю {total_messages} сообщений, пожалуйста, подождите",
    )

    for ref in refs_ids:
        success = await send_message_to_user(
            ref_id=ref,
            message=text,
            bot=bot,
            photo=photo,
        )
        if success:
            successfully_sent += 1
        await asyncio.sleep(0.1)

    result_message = f"Сообщений отправлено успешно: {successfully_sent} из {total_messages}"
    await callback.message.answer(result_message)


async def send_message_to_user(ref_id: int, message: str, bot: Bot, photo: str) -> bool:
    try:
        if photo:
            await bot.send_photo(photo=photo, caption=message, chat_id=ref_id)
        else:
            await bot.send_message(chat_id=ref_id, text=message)
        return True
    except TelegramRetryAfter as e:
        logger.error(
            f"Rate limit exceeded: retrying after {e.retry_after} "
            f"seconds for user with telegram_id {ref_id}",
        )
        await asyncio.sleep(e.retry_after)
        return await send_message_to_user(ref_id, message, bot, photo)
    except TelegramForbiddenError as e:
        logger.error(f"Failed to send message to user with telegram_id {ref_id}: {e}")
    except DetailedAiogramError as e:
        logger.error(f"Detailed Aiogram error for user with telegram_id={ref_id}: {e}")

    return False
