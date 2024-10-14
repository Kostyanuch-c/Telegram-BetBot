from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_RU_ERRORS


def check_referral_id_validator(text: str) -> str:
    if len(text.strip()) <= 6:
        raise ValueError(LEXICON_RU_ERRORS["error_input_referral_id"])
    if not text.strip().isdigit():
        raise ValueError(LEXICON_RU_ERRORS["error_is_not_digit"])
    return text
