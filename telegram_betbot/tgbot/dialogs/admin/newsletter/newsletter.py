import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import (
    DetailedAiogramError,
    TelegramForbiddenError,
    TelegramRetryAfter,
)
from aiogram.types import InlineKeyboardMarkup

from aiogram_dialog import DialogManager, ShowMode

from telegram_betbot.tgbot.keyboards.url_keyboard import create_keyboard_from_data


logger = logging.getLogger(__name__)


async def send_newsletter_message_to_admin_for_check(
    newsletter_data: dict,
    dialog_manager: DialogManager,
    admin_chat_id: int,
) -> None:
    text = newsletter_data.get("text")
    photo = newsletter_data.get("photo")

    keyboard_data = newsletter_data.get("keyboard_data", {})
    keyboard = create_keyboard_from_data(keyboard_data)

    dialog_manager.dialog_data["newsletter"] = newsletter_data
    bot: Bot = dialog_manager.middleware_data["bot"]

    if photo:
        await bot.send_photo(
            chat_id=admin_chat_id,
            photo=photo,
            caption=text,
            reply_markup=keyboard,
        )
    else:
        dialog_manager.show_mode = ShowMode.SEND
        await bot.send_message(chat_id=admin_chat_id, text=text, reply_markup=keyboard)


async def send_message_to_user(
    ref_id: int,
    message: str,
    bot: Bot,
    photo: str | None = None,
    keyboard: InlineKeyboardMarkup = None,
) -> bool:
    try:
        if photo:
            await bot.send_photo(
                photo=photo,
                caption=message,
                chat_id=ref_id,
                reply_markup=keyboard,
            )
        else:
            await bot.send_message(chat_id=ref_id, text=message, reply_markup=keyboard)
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
