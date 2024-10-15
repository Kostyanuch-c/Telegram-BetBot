import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_COMMANDS


logger = logging.getLogger(__name__)


async def set_main_menu_button(bot: Bot):
    # TODO сделать кнопки /support , /refresh и для админа /make_admin
    menu_commands = {
        "/help": LEXICON_COMMANDS["/help"],
        "/info": LEXICON_COMMANDS["/info"],
        "/bonus": LEXICON_COMMANDS["/bonus"],
    }
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description,
        )
        for command, description in menu_commands.items()
    ]
    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeDefault())
