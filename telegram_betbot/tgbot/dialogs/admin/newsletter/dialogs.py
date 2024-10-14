from aiogram.enums import ContentType

from aiogram_dialog import (
    Dialog,
    StartMode,
    Window,
)
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Next,
    Row,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from magic_filter import F

from telegram_betbot.tgbot.dialogs.admin.newsletter.getters import (
    get_data_check_newsletter_message,
    get_result_newsletter_message,
)
from telegram_betbot.tgbot.dialogs.admin.newsletter.handlers import (
    admin_button_clear_data_post,
    admin_choice_post_without_url_button,
    admin_correct_input_body_post_handler,
    admin_correct_input_photo_for_newsletter_handler,
    admin_correct_input_url_newsletter_handler,
    admin_send_newsletter,
    admin_wrong_type_input_photo_for_newsletter_handler,
)
from telegram_betbot.tgbot.dialogs.admin.newsletter.input_validator import (
    admin_check_input_text_and_url_validator,
    admin_check_text_newsletter_validator,
)
from telegram_betbot.tgbot.dialogs.commons.handlers import (
    send_error_message_handler,
    wrong_type_text_message_handler,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminNewsletterSG, AdminSG


admin_newsletter_dialog = Dialog(
    Window(
        Format(LEXICON_ADMIN["send_post_body"]),
        TextInput(
            id="input_body_post",
            type_factory=admin_check_text_newsletter_validator,
            on_success=admin_correct_input_body_post_handler,
            on_error=send_error_message_handler,
        ),
        MessageInput(
            func=wrong_type_text_message_handler,
            content_types=ContentType.ANY,
        ),
        Button(
            Const("◀️"),
            id="back",
            on_click=admin_button_clear_data_post,
            when=~F["dialog_data"]["newsletter"]["changing_mod"],
        ),
        SwitchTo(
            Const("◀️"),
            id="to_send_newsletter",
            state=AdminNewsletterSG.check_newsletter,
            when=F["dialog_data"]["newsletter"]["changing_mod"],
        ),
        state=AdminNewsletterSG.add_text_body_post,
    ),
    Window(
        Format(LEXICON_ADMIN["send_photo_prompt"]),
        MessageInput(
            func=admin_correct_input_photo_for_newsletter_handler,
            content_types=ContentType.PHOTO,
        ),
        MessageInput(
            func=admin_wrong_type_input_photo_for_newsletter_handler,
            content_types=ContentType.ANY,
        ),
        Next(
            Const(LEXICON_ADMIN["not_need_foto"]),
            id="next",
            when=~F["dialog_data"]["newsletter"]["changing_mod"],
        ),
        Back(Const("◀️"), id="back", when=~F["dialog_data"]["newsletter"]["changing_mod"]),
        SwitchTo(
            Const("◀️"),
            id="to_send_newsletter",
            state=AdminNewsletterSG.check_newsletter,
            when=F["dialog_data"]["newsletter"]["changing_mod"],
        ),
        state=AdminNewsletterSG.add_photo,
    ),
    Window(
        Format(LEXICON_ADMIN["send_url_text_and_link"]),
        TextInput(
            id="input_button_text_and_link",
            type_factory=admin_check_input_text_and_url_validator,
            on_success=admin_correct_input_url_newsletter_handler,
            on_error=send_error_message_handler,
        ),
        MessageInput(
            func=wrong_type_text_message_handler,
            content_types=ContentType.ANY,
        ),
        Button(
            Const(LEXICON_ADMIN["not_need_url_button"]),
            id="next",
            on_click=admin_choice_post_without_url_button,
            when=~F["dialog_data"]["newsletter"]["changing_mod"],
        ),
        Back(Const("◀️"), id="back", when=~F["dialog_data"]["newsletter"]["changing_mod"]),
        SwitchTo(
            Const("◀️"),
            id="to_send_newsletter",
            when=F["dialog_data"]["newsletter"]["changing_mod"],
            state=AdminNewsletterSG.check_newsletter,
        ),
        state=AdminNewsletterSG.add_url_button,
    ),
    Window(
        Format(LEXICON_ADMIN["confirmation_prompt"]),
        Button(Format(LEXICON_ADMIN["send_now"]), id="send_now", on_click=admin_send_newsletter),
        Row(
            SwitchTo(
                Const(LEXICON_ADMIN["change_text"]),
                id="to_create_body",
                state=AdminNewsletterSG.add_text_body_post,
            ),
            SwitchTo(
                text=Format("{work_with_photo}"),
                id="to_add_photo",
                state=AdminNewsletterSG.add_photo,
            ),
            Back(text=Format("{work_with_link}"), id="back"),
        ),
        Start(
            Const(LEXICON_ADMIN["newsletter_to_start"]),
            id="in_start",
            state=AdminSG.start,
            mode=StartMode.RESET_STACK,
        ),
        getter=get_data_check_newsletter_message,
        state=AdminNewsletterSG.check_newsletter,
    ),
    Window(
        Format(LEXICON_ADMIN["send_success"]),
        Start(
            Const(LEXICON_ADMIN["in_start"]),
            id="in_start",
            state=AdminSG.start,
            mode=StartMode.RESET_STACK,
        ),
        getter=get_result_newsletter_message,
        state=AdminNewsletterSG.end_send_newsletter,
    ),
)
