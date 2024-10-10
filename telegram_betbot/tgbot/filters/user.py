from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


def is_choice_button_for_referrals(
        data: dict[str:any],
        button: Button,
        dialog_manager: DialogManager,
) -> bool:
    return dialog_manager.dialog_data.get("is_referal", False)


def is_choice_button_for_new_user(
        data: dict[str:any],
        button: Button,
        dialog_manager: DialogManager,
) -> bool:
    return not dialog_manager.dialog_data.get("is_referal", False)
