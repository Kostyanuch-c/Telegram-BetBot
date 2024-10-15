from dataclasses import dataclass


@dataclass
class ReferralEntity:
    id: int  # noqa
    user_telegram_id: int
    bookmaker_id: int
    streamer_id: int
    referral_key: int
    is_confirmed: bool = False
