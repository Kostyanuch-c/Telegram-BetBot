from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Url
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.admin.getters import get_registration_link
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU
from telegram_betbot.tgbot.states.make_referal import MakeReferalSG


make_referal_finally_dialog = Dialog(
    Window(
        Format(LEXICON_RU["to_link"]),
        Url(
            text=Format("{streamer}"),
            url=Format("{registration_link}"),
            id="to_link",
        ),
        Back(Const("◀️"), id="back"),
        getter=get_registration_link,
        state=MakeReferalSG.check_referal_id,
    ),
)
