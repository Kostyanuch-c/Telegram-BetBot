from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from telegram_betbot.tgbot.states.start import StartSG


async def process_is_referal_choice(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    user_choice = button.widget_id
    dialog_manager.dialog_data["is_referal"] = True if user_choice == "yes_referal" else False
    await dialog_manager.next()


async def process_choice_bet_company(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    user_choice = button.widget_id
    dialog_manager.dialog_data["bet_company"] = user_choice
    await dialog_manager.next()


async def process_choice_streamer(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    user_choice = button.widget_id
    dialog_manager.dialog_data["streamer"] = user_choice

    if dialog_manager.dialog_data["is_referal"]:
        await dialog_manager.switch_to(state=StartSG.check_referal_id)
    else:
        await dialog_manager.next()


async def back_button_in_process_check_referal_id(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data["is_referal"]:
        await dialog_manager.switch_to(state=StartSG.choice_streamer)
    else:
        await dialog_manager.back()
