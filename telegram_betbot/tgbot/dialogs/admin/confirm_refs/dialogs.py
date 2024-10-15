from aiogram import F
from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.admin.confirm_refs.getters import admin_get_on_confirmed_refs
from telegram_betbot.tgbot.dialogs.admin.confirm_refs.handlers import (
    admin_correct_input_confirmed_refs_id_handler,
    button_all_not_confirmed_refs_handler,
)
from telegram_betbot.tgbot.dialogs.admin.confirm_refs.input_validators import (
    admin_check_confirmed_refs_id_validator,
)
from telegram_betbot.tgbot.dialogs.commons.getters import (
    get_bookmaker_and_streamer_names_from_start_data,
)
from telegram_betbot.tgbot.dialogs.commons.handlers import (
    send_error_message_handler,
    wrong_type_text_message_handler,
)
from telegram_betbot.tgbot.dialogs.commons.widgets import TO_START
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminConfirmRefs


admin_confirm_refs_dialog = Dialog(
    Window(
        Format(
            LEXICON_ADMIN["list_on_confirm_refs"],
            when=F["dialog_data"]["on_confirmed_refs"],
        ),
        Format(
            LEXICON_ADMIN["all_confirmed"],
            when=~F["dialog_data"]["on_confirmed_refs"],
        ),
        TextInput(
            id="input_link_or_id",
            type_factory=admin_check_confirmed_refs_id_validator,
            on_success=admin_correct_input_confirmed_refs_id_handler,
            on_error=send_error_message_handler,
        ),
        MessageInput(
            func=wrong_type_text_message_handler,
            content_types=ContentType.ANY,
        ),
        Button(
            Const(LEXICON_ADMIN["all_not_confirm_button"]),
            id="all_not_confirm",
            on_click=button_all_not_confirmed_refs_handler,
            when=F["dialog_data"]["on_confirmed_refs"],
        ),
        Cancel(Const("◀️"), id="back"),
        parse_mode="HTML",
        getter=admin_get_on_confirmed_refs,
        state=AdminConfirmRefs.send_confirms,
    ),
    Window(
        Format(
            LEXICON_ADMIN["all_not_confirm"],
        ),
        Back(Const(LEXICON_ADMIN["back"]), id="back"),
        TO_START,
        getter=get_bookmaker_and_streamer_names_from_start_data,
        state=AdminConfirmRefs.all_not_confirm_end,
    ),
    Window(
        Format(
            LEXICON_ADMIN["success_confirm_referral"],
        ),
        SwitchTo(Const(LEXICON_ADMIN["back"]), id="back", state=AdminConfirmRefs.send_confirms),
        TO_START,
        getter=get_bookmaker_and_streamer_names_from_start_data,
        state=AdminConfirmRefs.success_confirms_end,
    ),
)
