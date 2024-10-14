from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Next,
    Row,
    SwitchTo,
    Url,
)
from aiogram_dialog.widgets.text import (
    Case,
    Const,
    Format,
)

from magic_filter import F

from telegram_betbot.tgbot.dialogs.start.getters import (
    get_bookmaker_name,
    get_registration_link,
    get_start_message,
)
from telegram_betbot.tgbot.dialogs.start.handlers import (
    back_button_in_process_check_referal_id,
    correct_input_handler,
    error_input_id_handler,
    process_choice_bet_company,
    process_choice_streamer,
    process_is_referal_choice,
    wrong_type_input,
)
from telegram_betbot.tgbot.dialogs.start.input_validator import check_referral_id_validator
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU, LEXICON_START_MESSAGE
from telegram_betbot.tgbot.states.start import StartSG


start_dialog = Dialog(
    Window(
        Case(
            texts={
                "clear_user": Format(LEXICON_START_MESSAGE["base_message"]),
                "only_pari_pending": Format(LEXICON_START_MESSAGE["base_message"]),
                "only_upx_pending": Format(LEXICON_START_MESSAGE["base_message"]),
                "all_pending": Format(LEXICON_START_MESSAGE["start_with_all_pending_bm"]),
                "only_pari_confirm": Format(LEXICON_START_MESSAGE["base_message"]),
                "only_upx_confirm": Format(LEXICON_START_MESSAGE["base_message"]),
                "confirm_pari_pending_upx": Format(
                    LEXICON_START_MESSAGE["start_one_confirm_one_pending_bm"],
                ),
                "confirm_upx_pending_pari": Format(
                    LEXICON_START_MESSAGE["start_one_confirm_one_pending_bm"],
                ),
                "all_confirm": Format(LEXICON_START_MESSAGE["start_with_all_confirm_bm"]),
                ...: Format(LEXICON_START_MESSAGE["base_message"]),
            },
            selector="current_state_user",
        ),
        Row(
            Button(
                text=Const(LEXICON_RU["yes_referal"]),
                id="yes_referal",
                on_click=process_is_referal_choice,
            ),
            Button(
                text=Const(LEXICON_RU["no_make_referal"]),
                id="no_make_referal",
                on_click=process_is_referal_choice,
            ),
            when=~F["one_or_more_not_free"],
        ),
        Button(
            text=Format(LEXICON_RU["start_refresh_data_button"]),
            id="start_refresh_data_button",
            when=F["one_or_more_not_free"],
        ),
        getter=get_start_message,
        state=StartSG.start,
    ),
    Window(
        Format(LEXICON_RU["choice_bm"], when=~F["dialog_data"]["is_referal"]),
        Format(LEXICON_RU["choose_bookmaker_for_referal"], when=F["dialog_data"]["is_referal"]),
        Row(
            Button(text=Const("PARI"), id="Pari", on_click=process_choice_bet_company),
            Button(text=Const("Up-x"), id="Upx", on_click=process_choice_bet_company),
        ),
        Back(Const("◀️"), id="back"),
        state=StartSG.choice_bm,
    ),
    Window(
        Format(LEXICON_RU["choice_streamer"], when=~F["dialog_data"]["is_referal"]),
        Format(LEXICON_RU["choose_streamer_for_referal"], when=F["dialog_data"]["is_referal"]),
        Row(
            Button(text=Const("streamer_1"), id="streamer_1", on_click=process_choice_streamer),
            Button(text=Const("streamer_2"), id="streamer_2", on_click=process_choice_streamer),
            Button(text=Const("streamer_3"), id="streamer_3", on_click=process_choice_streamer),
        ),
        Back(Const("◀️"), id="back"),
        state=StartSG.choice_streamer,
    ),
    Window(
        Format(LEXICON_RU["to_link"]),
        Url(
            text=Format("{streamer}"),
            url=Format("{registration_link}"),
            id="to_link",
        ),
        Row(
            Back(Const("◀️"), id="back"),
            Next(Const("Я зарегистрировался"), id="after_registration"),
        ),
        getter=get_registration_link,
        state=StartSG.send_link,
    ),
    Window(
        Format(LEXICON_RU["request_id"]),
        TextInput(
            id="input_link_or_id",
            type_factory=check_referral_id_validator,
            on_success=correct_input_handler,
            on_error=error_input_id_handler,
        ),
        MessageInput(
            func=wrong_type_input,
            content_types=ContentType.ANY,
        ),
        Button(
            Const("◀️"),
            id="back_button_in_process_check_referal_id",
            on_click=back_button_in_process_check_referal_id,
        ),
        getter=get_bookmaker_name,
        state=StartSG.send_to_check_referal_id,
    ),
    Window(
        Format(LEXICON_RU["confirmation_success"]),
        SwitchTo(Const(LEXICON_RU["to_start"]), id="to_start", state=StartSG.start),
        state=StartSG.end_step,
    ),
)
