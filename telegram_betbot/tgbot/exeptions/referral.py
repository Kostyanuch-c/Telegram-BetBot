class ReferralInvalidError(Exception):
    @property
    def message(self) -> str:
        return (
            "🚫 <b>Неверный реферальный ключ</b> или"
            " он <b>не соответствует</b> стримеру/букмекеру.\n\n"
            "🔄 Возможно, моя база данных <b>еще не обновлена</b>, попробуйте позже.\n\n"
            "⚠️ Вы <b>не можете</b> быть рефералом у <b>нескольких стримеров</b> в одной конторе."
        )


class ReferralAlreadyRegisteredError(Exception):
    @property
    def message(self):
        return "🔒 Этот <b>реферальный ID</b> уже использован другим пользователем."


class ReferralAlreadyRegisteredByYouError(Exception):
    @property
    def message(self):
        return "ℹ️ Вы уже <b>зарегистрированы</b> с этим реферальным ключом."
