from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Next,
    Row,
    Url,
)
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.start.getters import get_registration_link, get_start_message
from telegram_betbot.tgbot.dialogs.start.handlers import (
    back_button_in_process_check_referal_id,
    process_choice_bet_company,
    process_choice_streamer,
    process_is_referal_choice,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU
from telegram_betbot.tgbot.states.start import StartSG


start_dialog = Dialog(
    Window(
        Format(LEXICON_RU["start"]),
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
        ),
        getter=get_start_message,
        state=StartSG.start,
    ),
    Window(
        Format(LEXICON_RU["choice_bm"]),
        Row(
            Button(text=Const("PARI BET"), id="pari_bet", on_click=process_choice_bet_company),
            Button(text=Const("Olimp Bet"), id="olimp_bet", on_click=process_choice_bet_company),
        ),
        Back(Const("◀️"), id="back"),
        getter=get_start_message,
        state=StartSG.choice_bm,
    ),
    Window(
        Format(LEXICON_RU["choice_streamer"]),
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
        Format("Отправь id для проверки"),
        Button(
            Const("◀️"),
            id="back_button_in_process_check_referal_id",
            on_click=back_button_in_process_check_referal_id,
        ),
        state=StartSG.check_referal_id,
    ),
)
