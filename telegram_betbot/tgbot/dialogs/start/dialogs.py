from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Next,
    Row,
    Url,
)
from aiogram_dialog.widgets.text import Const, Format

from magic_filter import F

from telegram_betbot.tgbot.dialogs.start.getters import (
    get_bookmaker_name,
    get_registration_link,
    get_start_message,
    get_streamer_chanel_link,
)
from telegram_betbot.tgbot.dialogs.start.handlers import (
    back_button_in_process_check_referal_id,
    check_input_type,
    correct_input_handler,
    error_input_id_handler,
    process_choice_bet_company,
    process_choice_streamer,
    process_is_referal_choice,
    to_start_after_check,
    wrong_type_input,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU
from telegram_betbot.tgbot.states.start import StartSG


start_dialog = Dialog(
    Window(
        Format(LEXICON_RU["start"], when=F["all_free"]),
        Format(LEXICON_RU["start_pari"], when=F["only_pari"]),
        Format(LEXICON_RU["start_upx"], when=F["only_upx"]),
        Format(LEXICON_RU["start_with_all_bm"], when=F["all_bm"]),
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
            when=F["one_or_more_free"],
        ),
        Url(
            text=Format(LEXICON_RU["start_pari_button"]),
            id="pari",
            url=Format("{pari_link}"),
            when=F["only_pary"],
        ),
        Url(
            text=Format(LEXICON_RU["start_upx_button"]),
            id="upx",
            url=Format("{upx_link}"),
            when=F["only_upx"],
        ),
        Row(
            Url(
                text=Format(LEXICON_RU["start_pari_button"]),
                id="pari",
                url=Format("{pari_link}"),
            ),
            Url(
                text=Format(LEXICON_RU["start_upx_button"]),
                id="upx",
                url=Format("{upx_link}"),
            ),
            when=F["all_bm"],
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
        getter=get_start_message,
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
        Format(LEXICON_RU["request_id"], when=~F["dialog_data"]["wrong_id"]),
        Format(LEXICON_RU["question_correct"], when=F["dialog_data"]["wrong_id"]),
        TextInput(
            id="input_link_or_id",
            type_factory=check_input_type,
            on_success=correct_input_handler,
            on_error=error_input_id_handler,
        ),
        MessageInput(
            func=wrong_type_input,
            content_types=ContentType.ANY,
        ),
        Next(
            Const("Да я уверен"),
            id="user_is_confident",
            when=F["dialog_data"]["wrong_id"],
        ),
        Button(
            Const("◀️"),
            id="back_button_in_process_check_referal_id",
            on_click=back_button_in_process_check_referal_id,
        ),
        getter=get_bookmaker_name,
        state=StartSG.check_referal_id,
    ),
    Window(
        Format(LEXICON_RU["waiting_for_confirmation"]),
        Button(
            Const("Вернуться в начало"),
            id="in_start",
            on_click=to_start_after_check,
        ),
        state=StartSG.wrong_check,
    ),
    Window(
        Format(LEXICON_RU["confirmation_success"]),
        Url(
            text=Format("Перейти в группу!"),
            url=Format("{channel_link}"),
            id="to_channel_link",
        ),
        Button(
            Const("Вернуться в начало"),
            id="in_start",
            on_click=to_start_after_check,
        ),
        getter=get_streamer_chanel_link,
        state=StartSG.good_check,
    ),
)
