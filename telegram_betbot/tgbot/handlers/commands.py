from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User

from aiogram_dialog import DialogManager, StartMode

from telegram_betbot.database import Database
from telegram_betbot.tgbot.services.user_service import UserService
from telegram_betbot.tgbot.states.start import StartSG


commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    db: Database,
) -> None:
    user: User = message.from_user

    user_data = {
        "telegram_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "telegram_date": message.date,
        "user_name": user.username,
    }

    await UserService(db).register_user(user_data)

    await dialog_manager.start(state=StartSG.choice_bm, mode=StartMode.RESET_STACK)
