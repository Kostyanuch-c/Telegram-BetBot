class ReferralAlreadyRegisteredError(Exception):
    @property
    def message(self):
        return "🔒 Этот <b>реферальный ID</b> уже использован другим пользователем."
