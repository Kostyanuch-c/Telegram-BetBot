from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Row,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.admin.newsletter.getters import get_data_check_newsletter_message
from telegram_betbot.tgbot.dialogs.admin.newsletter.handlers import (
    admin_button_clear_data_post,
    admin_choice_post_without_photo,
    admin_correct_input_body_post,
    admin_correct_input_photo_for_newsletter,
    admin_send_newsletter,
    admin_wrong_type_input_photo_for_newsletter,
)
from telegram_betbot.tgbot.dialogs.admin.start.getters import admin_get_start_message
from telegram_betbot.tgbot.dialogs.admin.start.handlers import (
    admin_check_input_type,
    admin_choice_bet_company,
    admin_choice_streamer,
    admin_error_input_handler,
    admin_wrong_type_input,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN
from telegram_betbot.tgbot.states.admin import AdminNewsletterSG


admin_newsletter_dialog = Dialog(
    Window(
        Format(LEXICON_ADMIN["choice_bm"]),
        Row(
            Button(text=Const("PARI"), id="Pari", on_click=admin_choice_bet_company),
            Button(text=Const("Up-x"), id="Upx", on_click=admin_choice_bet_company),
        ),
        Cancel(Const("◀️"), id="back"),
        getter=admin_get_start_message,
        state=AdminNewsletterSG.choice_bm,
    ),
    Window(
        Format(LEXICON_ADMIN["choice_streamer"]),
        Row(
            Button(text=Const("streamer_1"), id="streamer_1", on_click=admin_choice_streamer),
            Button(text=Const("streamer_2"), id="streamer_2", on_click=admin_choice_streamer),
            Button(text=Const("streamer_3"), id="streamer_3", on_click=admin_choice_streamer),
        ),
        Back(Const("◀️"), id="back"),
        state=AdminNewsletterSG.choice_streamer,
    ),
    Window(
        Format(LEXICON_ADMIN["send_post_body"]),
        TextInput(
            id="input_body_post",
            type_factory=admin_check_input_type,
            on_success=admin_correct_input_body_post,
            on_error=admin_error_input_handler,
        ),
        MessageInput(
            func=admin_wrong_type_input,
            content_types=ContentType.ANY,
        ),
        Button(Const("◀️"), id="back", on_click=admin_button_clear_data_post),
        state=AdminNewsletterSG.create_body_post,
    ),
    Window(
        Format(LEXICON_ADMIN["send_photo_prompt"]),
        MessageInput(
            func=admin_correct_input_photo_for_newsletter,
            content_types=ContentType.PHOTO,
        ),
        MessageInput(
            func=admin_wrong_type_input_photo_for_newsletter,
            content_types=ContentType.ANY,
        ),
        Button(Const("Фотография не нужна"), id="next", on_click=admin_choice_post_without_photo),
        Back(Const("Изменить сообщение"), id="back"),
        state=AdminNewsletterSG.add_photo,
    ),
    Window(
        Format(LEXICON_ADMIN["confirmation_prompt"]),
        Button(Format(LEXICON_ADMIN["send_now"]), id="send_now", on_click=admin_send_newsletter),
        Row(
            SwitchTo(
                Const("Изменить текст"),
                id="to_create_body",
                state=AdminNewsletterSG.create_body_post,
            ),
            Back(text=Format("{work_with_photo}"), id="to_add_photo"),
        ),
        getter=get_data_check_newsletter_message,
        state=AdminNewsletterSG.check_newsletter,
    ),
)
