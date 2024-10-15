import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent

from aiogram_dialog import DialogManager

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU_ERRORS


logger = logging.getLogger(__name__)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logger.error("Try delete old dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            LEXICON_RU_ERRORS["on_unknown_intent"],
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass
    # elif event.update.message:
    #     await event.update.message.answer(
    #         "Bot process was restarted due to maintenance.\n"
    #         "Redirecting to main menu.",
    #         reply_markup=ReplyKeyboardRemove(),
    #     )
