from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from telegram_betbot.tgbot.services.streamer_bookmaker_service import StreamerBookmakerService


async def admin_correct_input_link_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    url: str,
) -> None:
    db = dialog_manager.middleware_data["db"]
    bookmaker_id = dialog_manager.start_data["bookmaker_id"]
    streamer_id = dialog_manager.start_data["streamer_id"]

    await StreamerBookmakerService(db).update_or_create_referral_link(
        bookmaker_id=bookmaker_id,
        streamer_id=streamer_id,
        referral_link=url,
    )
    await dialog_manager.next()
