from aiogram_dialog import DialogManager


async def get_choice_data(dialog_manager: DialogManager, **kwargs):
    bookmaker = dialog_manager.dialog_data.get("bet_company")
    streamer = dialog_manager.dialog_data.get("streamer")

    return {
        "bookmaker": bookmaker,
        "streamer": streamer,
    }
