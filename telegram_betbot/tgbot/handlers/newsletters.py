from aiogram import F, Router
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, ShowMode

from telegram_betbot.database import Database
from telegram_betbot.tgbot.handlers.utils import to_start_dialog


newsletter_router = Router()
newsletter_router.message.filter(F.chat.type == "private")


@newsletter_router.callback_query(F.data.endswith("start_refresh_data_button"))
async def start_refresh_data_button(
    event: CallbackQuery,
    dialog_manager: DialogManager,
    db: Database,
):
    await to_start_dialog(
        db=db,
        dialog_manager=dialog_manager,
        user=event.from_user,
        show_mode=ShowMode.SEND,
    )
