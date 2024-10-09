from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User

from aiogram_dialog import DialogManager, StartMode

from telegram_betbot.database import Database
from telegram_betbot.tgbot.enums.role import Role
from telegram_betbot.tgbot.services.referral_service import ReferralService
from telegram_betbot.tgbot.services.user_service import UserService
from telegram_betbot.tgbot.states.admin import AdminSG
from telegram_betbot.tgbot.states.start import StartSG


commands_router = Router()


@commands_router.message(F.chat.type == "private", CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    db: Database,
) -> None:
    telegram_user: User = message.from_user

    user_data: dict[str, any] = {
        "telegram_id": telegram_user.id,
        "first_name": telegram_user.first_name,
        "last_name": telegram_user.last_name,
        "language_code": telegram_user.language_code,
        "user_name": telegram_user.username,
    }

    user_service: UserService = UserService(db)

    user_role: int = await user_service.get_role_or_create_user(user_data)

    if user_role == Role.ADMINISTRATOR:
        await dialog_manager.start(state=AdminSG.start, mode=StartMode.RESET_STACK)
    else:
        occupied_bookmakers, free_bookmakers = await ReferralService(db).check_free_bookmakers(
            telegram_id=telegram_user.id,
        )

        await dialog_manager.start(
            state=StartSG.start,
            mode=StartMode.RESET_STACK,
            data={
                "occupied_bookmakers": occupied_bookmakers,
                "free_bookmakers": free_bookmakers,
            },
        )
