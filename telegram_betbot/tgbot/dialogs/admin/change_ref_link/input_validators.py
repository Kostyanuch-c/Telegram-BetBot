from urllib.parse import urlparse

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN_ERRORS


def admin_check_type_link_validator(url: str) -> str:
    referral_link = urlparse(url)
    if not referral_link.scheme or not referral_link.netloc:
        raise ValueError(LEXICON_ADMIN_ERRORS["error_is_not_url"])
    return url
