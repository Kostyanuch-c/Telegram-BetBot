from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.text import Format

from telegram_betbot.tgbot.dialogs.start.getters import get_hello
from telegram_betbot.tgbot.states.start import StartSG


start_dialog = Dialog(
    Window(
        Format("Привет {username}!"),
        getter=get_hello,
        state=StartSG.start,
    ),
)
