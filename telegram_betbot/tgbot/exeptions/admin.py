class ReferralKeyUniqueError(Exception):
    def __init__(self, referral_key: str = ""):
        self.referral_key = referral_key

    @property
    def message(self) -> str:
        return f"Реферальный id {self.referral_key} уже существует."
