from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
)
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.admin.start.getters import get_choice_data
from telegram_betbot.tgbot.dialogs.admin.start.handlers import (
    admin_choice_add_referal_or_work_with_link,
    admin_choice_bet_company,
    admin_choice_streamer,
    check_input_type,
    correct_input_handler,
    error_input_handler,
    wrong_type_input,
)
from telegram_betbot.tgbot.dialogs.start.getters import get_start_message
from telegram_betbot.tgbot.filters.admin import is_choice_add_link, is_choice_add_referral
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminSG


admin_start_dialog = Dialog(
    Window(
        Format(LEXICON_ADMIN["start_admin"]),
        Row(
            Button(
                text=Const(LEXICON_ADMIN["add_referral_keys"]),
                id="add_referral_keys",
                on_click=admin_choice_add_referal_or_work_with_link,
            ),
            Button(
                text=Const(LEXICON_ADMIN["change_streamer_link"]),
                id="change_streamer_link",
                on_click=admin_choice_add_referal_or_work_with_link,
            ),
        ),
        getter=get_start_message,
        state=AdminSG.start,
    ),
    Window(
        Format(LEXICON_ADMIN["choice_bm"]),
        Row(
            Button(text=Const("PARI BET"), id="Pari", on_click=admin_choice_bet_company),
            Button(text=Const("Olimp Bet"), id="Olimp", on_click=admin_choice_bet_company),
        ),
        Back(Const("◀️"), id="back"),
        getter=get_start_message,
        state=AdminSG.choice_bm,
    ),
    Window(
        Format(LEXICON_ADMIN["choice_streamer"]),
        Row(
            Button(text=Const("streamer_1"), id="streamer_1", on_click=admin_choice_streamer),
            Button(text=Const("streamer_2"), id="streamer_2", on_click=admin_choice_streamer),
            Button(text=Const("streamer_3"), id="streamer_3", on_click=admin_choice_streamer),
        ),
        Back(Const("◀️"), id="back"),
        getter=get_start_message,
        state=AdminSG.choice_streamer,
    ),
    Window(
        Format(
            LEXICON_ADMIN["add_referral_info"],
            when=is_choice_add_referral,
        ),
        Format(
            LEXICON_ADMIN["change_link_info"],
            when=is_choice_add_link,
        ),
        TextInput(
            id="input_link_or_id",
            type_factory=check_input_type,
            on_success=correct_input_handler,
            on_error=error_input_handler,
        ),
        MessageInput(
            func=wrong_type_input,
            content_types=ContentType.ANY,
        ),
        Back(Const("◀️"), id="back"),
        parse_mode="HTML",
        getter=get_choice_data,
        state=AdminSG.main_changedsd,
    ),
)
