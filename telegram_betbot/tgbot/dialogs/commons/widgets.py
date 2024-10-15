from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const

from magic_filter import F

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminNewsletterSG, AdminSG


TO_START = Start(
    Const(LEXICON_ADMIN["in_start"]),
    id="in_start",
    state=AdminSG.start,
    mode=StartMode.RESET_STACK,
)

SWITCH_TO_NEWSLETTER = SwitchTo(
    Const("◀️"),
    id="to_send_newsletter",
    state=AdminNewsletterSG.check_newsletter,
    when=F["dialog_data"]["newsletter"]["changing_mod"],
)
