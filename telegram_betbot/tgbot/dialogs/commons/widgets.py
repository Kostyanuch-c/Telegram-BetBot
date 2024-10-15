from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminSG


TO_START = Start(
    Const(LEXICON_ADMIN["in_start"]),
    id="in_start",
    state=AdminSG.start,
    mode=StartMode.RESET_STACK,
)
