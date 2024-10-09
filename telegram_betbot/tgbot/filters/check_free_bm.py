from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


def is_one_or_more_free_bm(data: dict[str:any], button: Button, dialog_manager: DialogManager):
    return len(dialog_manager.dialog_data.get("free_bookmakers", [])) >= 1


def free_only_pari(data: dict[str:any], button: Button, dialog_manager: DialogManager):
    return dialog_manager.dialog_data["occupied_bookmakers"].get(
        "Pari", False,
    ) and not dialog_manager.dialog_data["occupied_bookmakers"].get("Olimp", False)


def free_only_olimp(data: dict[str:any], button: Button, dialog_manager: DialogManager):
    return dialog_manager.dialog_data["occupied_bookmakers"].get(
        "Olimp", False,
    ) and not dialog_manager.dialog_data["occupied_bookmakers"].get("Pari", False)


def is_not_free_bm(data: dict[str:any], button: Button, dialog_manager: DialogManager):
    return dialog_manager.dialog_data.get("free_bookmakers", []) == []
