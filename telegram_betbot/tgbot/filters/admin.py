from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


def is_choice_add_referral(data: dict[str:any], button: Button, dialog_manager: DialogManager):
    return dialog_manager.dialog_data.get("add_referal")


def is_choice_add_link(data: dict[str:any], button: Button, dialog_manager: DialogManager):
    return not dialog_manager.dialog_data.get("add_referal")
