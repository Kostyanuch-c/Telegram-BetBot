from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Row,
    Start,
)
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.admin.start.getters import admin_get_start_message
from telegram_betbot.tgbot.dialogs.admin.start.handlers import (
    admin_choice_bet_company,
    admin_choice_streamer,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminChoiceBmAndStreamer, AdminSG


admin_start_dialog = Dialog(
    Window(
        Format(LEXICON_ADMIN["start_admin"]),
        Row(
            Start(
                text=Const(LEXICON_ADMIN["confirm_referrals"]),
                id="confirm_referrals",
                data={"confirm_referrals": True},
                state=AdminChoiceBmAndStreamer.choice_bm,
            ),
            Start(
                text=Const(LEXICON_ADMIN["change_streamer_link"]),
                id="change_streamer_link",
                data={"change_streamer_link": True},
                state=AdminChoiceBmAndStreamer.choice_bm,
            ),
        ),
        Start(
            text=Const(LEXICON_ADMIN["make_newsletter"]),
            state=AdminChoiceBmAndStreamer.choice_bm,
            data={"make_newsletter": True},
            id="make_newsletter",
        ),
        getter=admin_get_start_message,
        state=AdminSG.start,
    ),
)

admin_choice_bm_and_streamer = Dialog(
    Window(
        Format(LEXICON_ADMIN["choice_bm"]),
        Row(
            Button(text=Const("PARI"), id="Pari", on_click=admin_choice_bet_company),
            Button(text=Const("Up-x"), id="Upx", on_click=admin_choice_bet_company),
        ),
        Cancel(Const("◀️"), id="back"),
        state=AdminChoiceBmAndStreamer.choice_bm,
    ),
    Window(
        Format(LEXICON_ADMIN["choice_streamer"]),
        Row(
            Button(text=Const("streamer_1"), id="streamer_1", on_click=admin_choice_streamer),
            Button(text=Const("streamer_2"), id="streamer_2", on_click=admin_choice_streamer),
            Button(text=Const("streamer_3"), id="streamer_3", on_click=admin_choice_streamer),
        ),
        Back(Const("◀️"), id="back"),
        state=AdminChoiceBmAndStreamer.choice_streamer,
    ),
)
