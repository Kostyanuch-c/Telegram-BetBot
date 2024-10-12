from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button

from telegram_betbot.tgbot.exeptions.referral import (
    ReferralAlreadyRegisteredByYouError,
    ReferralAlreadyRegisteredError,
    ReferralInvalidError,
)
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU_ERRORS
from telegram_betbot.tgbot.services.referral_service import ReferralService
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

    free_bookmakers = dialog_manager.dialog_data["free_bookmakers"]

    if user_choice in free_bookmakers:
        dialog_manager.dialog_data["bet_company"] = user_choice

        await dialog_manager.next()
    else:
        await callback.answer(text=LEXICON_RU_ERRORS['choice_not_free_bm'])


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


async def error_input_id_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError,
):
    await message.answer(text=LEXICON_RU_ERRORS['error_input_referral_id'])


async def wrong_type_input(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.answer(text=LEXICON_RU_ERRORS['wrong_type_input_referral_id'])


async def correct_input_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        referral_key: str,
) -> None:
    db = dialog_manager.middleware_data["db"]
    bookmaker = dialog_manager.dialog_data["bet_company"]
    streamer = dialog_manager.dialog_data["streamer"]
    telegram_id = message.from_user.id
    try:
        await ReferralService(db).check_and_create_referral(
            referral_key=referral_key,
            telegram_id=telegram_id,
            bookmaker_name=bookmaker,
            streamer_name=streamer,
        )
        free_bookmakers = dialog_manager.dialog_data["free_bookmakers"]
        occupied_bookmakers = dialog_manager.dialog_data["occupied_bookmakers"]
        if bookmaker in free_bookmakers:
            free_bookmakers.remove(bookmaker)

        occupied_bookmakers[bookmaker] = streamer

        dialog_manager.dialog_data.update(
            {
                "free_bookmakers": free_bookmakers,
                "occupied_bookmakers": occupied_bookmakers,
            },
        )

        await dialog_manager.switch_to(state=StartSG.good_check)
    except ReferralInvalidError as exception:
        dialog_manager.dialog_data["wrong_id"] = True
        await message.answer(exception.message)

    except ReferralAlreadyRegisteredByYouError as exception:
        await message.answer(exception.message)

    except ReferralAlreadyRegisteredError as exception:
        await message.answer(exception.message)


async def to_start_after_check(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["wrong_id"] = False
    await dialog_manager.switch_to(state=StartSG.start)
