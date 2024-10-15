import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_COMMANDS


logger = logging.getLogger(__name__)


def _create_menu_commands(menu_commands: dict[str, str]) -> list[BotCommand]:
    return [
        BotCommand(command=command, description=description)
        for command, description in menu_commands.items()
    ]


async def set_admin_menu_button(bot: Bot):
    admin_commands = {
        "/make_admin": LEXICON_COMMANDS["/make_admin"],
    }
    main_menu_commands = _create_menu_commands(admin_commands)
    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeDefault())


async def set_main_menu_button(bot: Bot):
    user_commands = {
        "/help": LEXICON_COMMANDS["/help"],
        "/support": LEXICON_COMMANDS["/support"],
        "/refresh": LEXICON_COMMANDS["/refresh"],
    }
    main_menu_commands = _create_menu_commands(user_commands)
    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeDefault())
