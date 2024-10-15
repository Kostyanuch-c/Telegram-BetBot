from urllib.parse import urlparse

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN_ERRORS


def admin_check_text_newsletter_validator(text: str) -> str:
    if isinstance(text, str) and len(text.strip()) > 1:
        return text
    raise ValueError(LEXICON_ADMIN_ERRORS["small_text"])


def admin_check_input_text_and_url_validator(text: str) -> str:
    words_list = text.strip().split("\n")
    if len(words_list) != 2:
        raise ValueError(LEXICON_ADMIN_ERRORS["error_invalid_format"])

    button_text, url = words_list

    if len(button_text) < 2:
        raise ValueError(LEXICON_ADMIN_ERRORS["error_invalid_button_text"])

    referral_link = urlparse(url)
    if not referral_link.scheme or not referral_link.netloc:
        raise ValueError(LEXICON_ADMIN_ERRORS["error_is_not_url"])
    return text
