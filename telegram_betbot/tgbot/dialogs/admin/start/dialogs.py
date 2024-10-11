from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from magic_filter import F

from telegram_betbot.tgbot.dialogs.admin.start.getters import (
    admin_get_choice_data,
    admin_get_start_message,
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
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminNewsletterSG, AdminSG


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
        Start(
            text=Const(LEXICON_ADMIN["make_newsletter"]),
            state=AdminNewsletterSG.choice_bm,
            id="make_newsletter",
        ),
        getter=admin_get_start_message,
        state=AdminSG.start,
    ),
    Window(
        Format(LEXICON_ADMIN["choice_bm"]),
        Row(
            Button(text=Const("PARI"), id="Pari", on_click=admin_choice_bet_company),
            Button(text=Const("Up-x"), id="Upx", on_click=admin_choice_bet_company),
        ),
        Back(Const("◀️"), id="back"),
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
        state=AdminSG.choice_streamer,
    ),
    Window(
        Format(
            LEXICON_ADMIN["add_referral_info"],
            when=F["dialog_data"]["add_referal"],
        ),
        Format(
            LEXICON_ADMIN["change_link_info"],
            when=~F["dialog_data"]["add_referal"],
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
        getter=admin_get_choice_data,
        state=AdminSG.main_change,
    ),
    Window(
        Format(
            LEXICON_ADMIN["success_add_referral"],
            when=F["dialog_data"]["add_referal"],
        ),
        Format(
            LEXICON_ADMIN["success_add_link"],
            when=~F["dialog_data"]["add_referal"],
        ),
        Back(Const(LEXICON_ADMIN["back"]), id="back"),
        SwitchTo(Const(LEXICON_ADMIN["in_start"]), id="in_start", state=AdminSG.start),
        parse_mode="HTML",
        getter=admin_get_choice_data,
        state=AdminSG.end_step,
    ),
)
