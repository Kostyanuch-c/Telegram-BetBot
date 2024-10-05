from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    Url,
)
from aiogram_dialog.widgets.text import Const, Format

from telegram_betbot.tgbot.dialogs.start.getters import get_registration_link, get_start_message
from telegram_betbot.tgbot.dialogs.start.handlers import (
    process_choice_bet_company,
    process_choice_streamer,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU
from telegram_betbot.tgbot.states.start import StartSG


start_dialog = Dialog(
    Window(
        Format(LEXICON_RU["start_choice_bm"]),
        Row(
            Button(text=Const("PARI BET"), id="pari_bet", on_click=process_choice_bet_company),
            Button(text=Const("Olimp Bet"), id="olimp_bet", on_click=process_choice_bet_company),
        ),
        getter=get_start_message,
        state=StartSG.choice_bm,
    ),
    Window(
        Format(LEXICON_RU["streamers"]),
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
        # URL будет генерироваться динамически через getter
        Url(
            text=Format("{streamer}"),
            url=Format("{registration_link}"),  # Используем ссылку, возвращенную из getter
            id="to_link",
        ),
        Back(Const("◀️"), id="back"),
        getter=get_registration_link,
        state=StartSG.send_link,
    ),
)
