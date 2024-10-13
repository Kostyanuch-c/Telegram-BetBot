from aiogram.enums import ContentType

from aiogram_dialog import (
    Dialog,
    StartMode,
    Window,
)
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Cancel, Start
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.admin.change_ref_link.handlers import (
    admin_correct_input_link_handler,
)
from telegram_betbot.tgbot.dialogs.admin.change_ref_link.input_validators import (
    admin_check_type_link_validator,
)
from telegram_betbot.tgbot.dialogs.commons.getters import (
    get_bookmaker_and_streamer_names_from_start_data,
)
from telegram_betbot.tgbot.dialogs.commons.handlers import (
    send_error_message_handler,
    wrong_type_text_message_handler,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminChangeRefsLink, AdminSG


admin_change_link_dialog = Dialog(
    Window(
        Format(
            LEXICON_ADMIN["change_link_info"],
        ),
        TextInput(
            id="input_link_or_id",
            type_factory=admin_check_type_link_validator,
            on_success=admin_correct_input_link_handler,
            on_error=send_error_message_handler,
        ),
        MessageInput(
            func=wrong_type_text_message_handler,
            content_types=ContentType.ANY,
        ),
        Cancel(Const("◀️"), id="back"),
        getter=get_bookmaker_and_streamer_names_from_start_data,
        state=AdminChangeRefsLink.send_link,
    ),
    Window(
        Format(
            LEXICON_ADMIN["success_add_link"],
        ),
        Start(
            Const(LEXICON_ADMIN["in_start"]),
            id="in_start",
            state=AdminSG.start,
            mode=StartMode.RESET_STACK,
        ),
        getter=get_bookmaker_and_streamer_names_from_start_data,
        state=AdminChangeRefsLink.end_change_link,
    ),
)
