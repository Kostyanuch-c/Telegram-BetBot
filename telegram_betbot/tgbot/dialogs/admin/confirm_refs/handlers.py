import asyncio

from aiogram import Bot
from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from telegram_betbot.tgbot.dialogs.admin.newsletter.newsletter import send_message_to_user
from telegram_betbot.tgbot.exeptions.admin import ReferralUpdateStatusError
from telegram_betbot.tgbot.keyboards.callback import make_inline_button_keyboard
from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN, LEXICON_ADMIN_ERRORS
from telegram_betbot.tgbot.services.referral_service import ReferralService


async def admin_correct_input_confirmed_refs_id_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    confirmed_referrals_keys: set[str],
) -> None:
    """Handler for correct send keys admin and send message users about result checked"""
    db = dialog_manager.middleware_data["db"]

    bookmaker_id = dialog_manager.start_data["bookmaker_id"]
    streamer_id = dialog_manager.start_data["streamer_id"]

    on_confirmed_refs_keys_dict: dict[str, int] = dialog_manager.dialog_data["on_confirmed_refs"]
    on_confirmed_refs_keys_set = set(on_confirmed_refs_keys_dict)

    if confirmed_referrals_keys <= on_confirmed_refs_keys_set:
        try:
            await ReferralService(db).update_referral_status(
                bookmaker_id=bookmaker_id,
                streamer_id=streamer_id,
                referral_keys=list(map(int, confirmed_referrals_keys)),
            )
            bot: Bot = dialog_manager.middleware_data["bot"]
            await notify_users(
                bot=bot,
                referral_keys=confirmed_referrals_keys,
                refs_dict=on_confirmed_refs_keys_dict,
                success=True,
            )
            not_confirmed_referrals_keys = on_confirmed_refs_keys_set - confirmed_referrals_keys
            await notify_users(
                bot=bot,
                referral_keys=not_confirmed_referrals_keys,
                refs_dict=on_confirmed_refs_keys_dict,
                success=False,
            )
            # TODO Cделать удаление из базы данных не прошедших проверку реферралов

            await dialog_manager.next()
        except ReferralUpdateStatusError as exception:
            await message.answer(exception.message)
    else:
        await handle_missing_keys(
            message=message,
            confirmed_keys=confirmed_referrals_keys,
            on_confirmed_keys=on_confirmed_refs_keys_set,
        )


async def notify_users(
    bot: Bot,
    referral_keys: set[str],
    refs_dict: dict[str, int],
    success: bool,
) -> None:
    message = (
        LEXICON_ADMIN["positive_confirmation"]
        if success
        else LEXICON_ADMIN["negative_confirmation"]
    )
    keyboard = make_inline_button_keyboard(
        callback_data="start_refresh_data_button",
        text=LEXICON_ADMIN["update_data"],
    )
    for key in referral_keys:
        await send_message_to_user(
            bot=bot,
            message=message,
            ref_id=refs_dict[key],
            keyboard=keyboard,
        )
        await asyncio.sleep(0.05)


async def handle_missing_keys(
    message: Message,
    confirmed_keys: set[str],
    on_confirmed_keys: set[str],
) -> None:
    missing_keys = confirmed_keys - on_confirmed_keys
    output_missing_keys = "\n".join(missing_keys)
    await message.answer(
        f"{LEXICON_ADMIN_ERRORS['not_in_list_refs']}\n\n"
        f"{output_missing_keys}\n\n"
        f"{LEXICON_ADMIN_ERRORS['request_send_new_ids']}",
    )
