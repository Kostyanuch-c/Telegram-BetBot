from aiogram_dialog import DialogManager


async def get_bookmaker_and_streamer_names_from_start_data(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict:
    bookmaker = dialog_manager.start_data.get("bet_company")
    streamer = dialog_manager.start_data.get("streamer")

    return {
        "bookmaker": bookmaker,
        "streamer": streamer,
    }


#
# async def get_bookmaker_and_streamer_names_from_dialog_data(
#     dialog_manager: DialogManager,
#     **kwargs,
# ) -> dict:
#     bookmaker = dialog_manager.dialog_data.get("bet_company")
#     streamer = dialog_manager.dialog_data.get("streamer")
#
#     return {
#         "bookmaker": bookmaker,
#         "streamer": streamer,
#     }
