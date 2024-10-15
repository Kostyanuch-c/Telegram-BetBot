from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)

from telegram_betbot.database import Database
from telegram_betbot.tgbot.enums.role import Role
from telegram_betbot.tgbot.handlers.utils import extract_user_data, to_start_dialog
from telegram_betbot.tgbot.keyboards.menu_button import set_admin_menu_button, set_main_menu_button
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_COMMANDS_RESPONSES
from telegram_betbot.tgbot.services.user_service import UserService
from telegram_betbot.tgbot.states.admin import AdminSG


commands_router = Router()
commands_router.message.filter(F.chat.type == "private")


@commands_router.message(CommandStart())
async def process_start_command(
    event: Message,
    dialog_manager: DialogManager,
    db: Database,
) -> None:
    bot = dialog_manager.middleware_data["bot"]
    user = event.from_user

    user_data = extract_user_data(telegram_user=user)

    user_role = await UserService(db).get_role_or_create_user(user_data)
    if user_role == Role.ADMINISTRATOR:
        await set_admin_menu_button(bot)
        await dialog_manager.start(state=AdminSG.start, mode=StartMode.RESET_STACK)

    else:
        await set_main_menu_button(bot)
        await to_start_dialog(db=db, dialog_manager=dialog_manager, user=user)


@commands_router.message(Command(commands="refresh"))
async def process_refresh_command(
    event: Message,
    dialog_manager: DialogManager,
    db: Database,
):
    await event.answer(LEXICON_COMMANDS_RESPONSES["refresh"])
    await to_start_dialog(
        db=db,
        dialog_manager=dialog_manager,
        user=event.from_user,
        show_mode=ShowMode.SEND,
    )


@commands_router.message(Command(commands="help"))
async def process_help_command(
    event: Message,
    dialog_manager: DialogManager,
    db: Database,
):
    await event.answer(LEXICON_COMMANDS_RESPONSES["help"])
    dialog_manager.show_mode = ShowMode.NO_UPDATE


@commands_router.message(Command(commands="support"))
async def process_support_command(
    event: Message,
    dialog_manager: DialogManager,
    db: Database,
):
    await event.answer(LEXICON_COMMANDS_RESPONSES["support"])
    dialog_manager.show_mode = ShowMode.NO_UPDATE


@commands_router.message(Command(commands="make_admin"))
async def process_make_admin_command(
    event: Message,
    dialog_manager: DialogManager,
    db: Database,
):
    user = event.from_user
    user_data = extract_user_data(telegram_user=user)

    user_role = await UserService(db).get_role_or_create_user(user_data)
    if user_role != Role.ADMINISTRATOR:
        await dialog_manager.update({}, show_mode=ShowMode.SEND)
        return

    try:
        new_admin_id = int(event.text.split()[1])
    except (IndexError, ValueError):
        await event.answer(LEXICON_COMMANDS_RESPONSES["invalid_telegram_id"])
        return

    new_admin_data = await UserService(db).get_user_by_telegram_id(new_admin_id)
    if not new_admin_data:
        await event.answer(
            LEXICON_COMMANDS_RESPONSES["user_not_found"].format(user_id=new_admin_id),
        )
        return

    await UserService(db).update_user_role(new_admin_data.telegram_id, Role.ADMINISTRATOR)

    await event.answer(LEXICON_COMMANDS_RESPONSES["admin_assigned"].format(user_id=new_admin_id))
    await dialog_manager.update({}, show_mode=ShowMode.SEND)
