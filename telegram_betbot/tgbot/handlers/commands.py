from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)

from telegram_betbot.database import Database
from telegram_betbot.tgbot.enums.role import Role
from telegram_betbot.tgbot.handlers.utils import check_free_bookmakers, extract_user_data
from telegram_betbot.tgbot.services.user_service import UserService
from telegram_betbot.tgbot.states.admin import AdminSG
from telegram_betbot.tgbot.states.start import StartSG


commands_router = Router()
commands_router.message.filter(F.chat.type == "private")


@commands_router.callback_query(F.data.endswith("start_refresh_data_button"))
async def start_refresh_data_button(
    event: CallbackQuery,
    dialog_manager: DialogManager,
    db: Database,
):
    occupied_bookmakers, free_bookmakers = await check_free_bookmakers(
        db=db,
        dialog_manager=dialog_manager,
        user=event.from_user,
    )

    dialog_manager.dialog_data.update(
        {
            "occupied_bookmakers": occupied_bookmakers,
            "free_bookmakers": free_bookmakers,
        },
    )

    await dialog_manager.update({}, show_mode=ShowMode.SEND)


# @commands_router.message(Command(commands="refresh"))
# async def process_refresh_command(
#         event: Message,
#         dialog_manager: DialogManager,
#         db: Database,
# ):
#     await event.answer("Данные обновленны")
#     dialog_manager.show_mode = ShowMode.SEND
#     await to_start_dialog(db=db, dialog_manager=dialog_manager, user=event.from_user)


@commands_router.message(CommandStart())
async def process_start_command(
    event: Message,
    dialog_manager: DialogManager,
    db: Database,
) -> None:
    user = event.from_user

    user_data = extract_user_data(telegram_user=user)

    user_role = await UserService(db).get_role_or_create_user(user_data)
    if user_role == Role.ADMINISTRATOR:
        await dialog_manager.start(state=AdminSG.start, mode=StartMode.RESET_STACK)

    else:
        occupied_bookmakers, free_bookmakers = await check_free_bookmakers(
            db=db,
            dialog_manager=dialog_manager,
            user=user,
        )

        await dialog_manager.start(
            state=StartSG.start,
            mode=StartMode.RESET_STACK,
            data={
                "occupied_bookmakers": occupied_bookmakers,
                "free_bookmakers": free_bookmakers,
            },
        )
