from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def process_choice_bet_company(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
):
    user_choice = button.widget_id
    dialog_manager.dialog_data["bet_company"] = user_choice
    await dialog_manager.next()


async def process_choice_streamer(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
):
    user_choice = button.widget_id
    dialog_manager.dialog_data["streamer"] = user_choice
    await dialog_manager.next()


# async def process_send_link(callback: CallbackQuery,
# button: Button, dialog_manager: DialogManager):
#     user_choice = button.widget_id
