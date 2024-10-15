from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def make_url_inline_button_keyboard(url: str, text: str) -> InlineKeyboardMarkup:
    url_button = InlineKeyboardButton(text=text, url=url)
    return InlineKeyboardMarkup(inline_keyboard=[[url_button]])


def create_keyboard_from_data(keyboard_data: dict) -> InlineKeyboardMarkup | None:
    if not keyboard_data:
        return

    url = keyboard_data.get("url")
    text = keyboard_data.get("text")

    if url and text:
        return make_url_inline_button_keyboard(url=url, text=text)
