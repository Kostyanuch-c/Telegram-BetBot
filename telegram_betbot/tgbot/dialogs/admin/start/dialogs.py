from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.admin.start.getters import (
    admin_get_start_message,
    get_choice_data,
)
from telegram_betbot.tgbot.dialogs.admin.start.handlers import (
    admin_check_input_type,
    admin_choice_add_referal_or_work_with_link,
    admin_choice_bet_company,
    admin_choice_streamer,
    admin_correct_input_handler,
    admin_error_input_handler,
    admin_wrong_type_input,
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
        getter=admin_get_start_message,
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
            type_factory=admin_check_input_type,
            on_success=admin_correct_input_handler,
            on_error=admin_error_input_handler,
        ),
        MessageInput(
            func=admin_wrong_type_input,
            content_types=ContentType.ANY,
        ),
        Back(Const("◀️"), id="back"),
        parse_mode="HTML",
        getter=get_choice_data,
        state=AdminSG.main_change,
    ),
    Window(
        Format(
            LEXICON_ADMIN["success_add_referral"],
            when=is_choice_add_referral,
        ),
        Format(
            LEXICON_ADMIN["success_add_link"],
            when=is_choice_add_link,
        ),
        Back(Const(LEXICON_ADMIN["back"]), id="back"),
        SwitchTo(Const(LEXICON_ADMIN["in_start"]), id="in_start", state=AdminSG.start),
        parse_mode="HTML",
        getter=get_choice_data,
        state=AdminSG.end_step,
    ),
)
