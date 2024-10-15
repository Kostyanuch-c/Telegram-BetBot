from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN_ERRORS


async def wrong_type_text_message_handler(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    await message.answer(text=LEXICON_ADMIN_ERRORS["error_wrong_type_input"])


async def send_error_message_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(text=str(error))
