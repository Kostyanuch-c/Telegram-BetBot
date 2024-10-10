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


def is_all_bm_free(data: dict[str:any], button: Button, dialog_manager: DialogManager) -> bool:
    return len(dialog_manager.dialog_data.get("free_bookmakers", [])) == 2


def is_one_or_more_free_bm(
    data: dict[str:any],
    button: Button,
    dialog_manager: DialogManager,
) -> bool:
    return len(dialog_manager.dialog_data.get("free_bookmakers", [])) >= 1


def free_only_pari(data: dict[str:any], button: Button, dialog_manager: DialogManager) -> bool:
    occupied = dialog_manager.dialog_data["occupied_bookmakers"]
    return occupied.get("Pari", False) and not occupied.get("Upx", False)


def free_only_upx(data: dict[str:any], button: Button, dialog_manager: DialogManager) -> bool:
    occupied = dialog_manager.dialog_data["occupied_bookmakers"]
    return occupied.get("Upx", False) and not occupied.get("Pari", False)


def is_not_free_bm(data: dict[str:any], button: Button, dialog_manager: DialogManager) -> bool:
    return dialog_manager.dialog_data.get("free_bookmakers", []) == []
