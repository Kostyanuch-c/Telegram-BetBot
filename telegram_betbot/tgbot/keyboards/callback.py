from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def make_inline_button_keyboard(callback_data: str, text: str) -> InlineKeyboardMarkup:
    inline_button = InlineKeyboardButton(text=text, callback_data=callback_data)
    return InlineKeyboardMarkup(inline_keyboard=[[inline_button]])
