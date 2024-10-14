import re

from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_ADMIN_ERRORS


def admin_check_confirmed_refs_id_validator(text: str) -> set[str]:
    referrals_keys = re.split(r"[\s]+", text.strip())

    if all(x.isdigit() for x in referrals_keys):
        return set(referrals_keys)

    raise ValueError(LEXICON_ADMIN_ERRORS["error_input_referral_id"])
