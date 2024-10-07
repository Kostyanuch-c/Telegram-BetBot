from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button


async def admin_choice_add_referal_or_work_with_link(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["add_referal"] = (
        True if button.widget_id == "add_referral_keys" else False
    )
    await dialog_manager.next()


async def admin_choice_bet_company(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    admin_choice = button.widget_id
    dialog_manager.dialog_data["bet_company"] = admin_choice
    await dialog_manager.next()


async def admin_choice_streamer(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    admin_choice = button.widget_id
    dialog_manager.dialog_data["streamer"] = admin_choice

    await dialog_manager.next()


def check_input_type(text: any) -> str:
    if isinstance(text, str) and len(text.strip()) > 1:
        return text
    raise ValueError


async def correct_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
) -> None:
    dialog_manager.dialog_data["bet_company"]
    dialog_manager.dialog_data["streamer"]

    if dialog_manager.dialog_data.get("add_referal", False):
        await message.answer(text=f"Вам {text}")  # сделать добавление в бд рефереральной id
    else:
        await message.answer(text=f"Вам {text}")


async def error_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(
        text="Вы ввели некорректные данные. Сообщение должно быть строкой, больше одного символа!",
    )


async def wrong_type_input(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.answer(text="Введите, пожалуйста, текстовое сообщение.")
