LEXICON_COMMANDS: dict[str, str] = {
    "/help": "Список доступных комманд",
    "/info": "Информация о текущих подписках.",
    "/bonus": "Узнать про бонусы",
}
BOOKMAKER_LINKS: dict[str, str] = {
    "pari_name": "PARI",
    "pari_bet": {
        "streamer_1": "https://pari.ru/",
        "streamer_2": "https://pari.ru/",
        "streamer_3": "https://pari.ru/",
    },
    "olimp_name": "OLIMP",
    "olimp_bet": {
        "streamer_1": "https://www.olimp.bet/",
        "streamer_2": "https://www.olimp.bet/",
        "streamer_3": "https://www.olimp.bet/",
    },
}

LEXICON_ADMIN: dict[str, str] = {
    "start_admin": "Здравстуйте хозяин {username}",
    "add_referral_keys": "Добавить id новых рефералов",
    "change_streamer_link": "Изменить/добавить реферальную ссылку",
    "choice_bm": "Выбери букмекера",
    "choice_streamer": "Выбери стримера",
    "add_referral_info": "<b>Введите новые реферральные id для {streamer} в {bookmaker} </b>",
    "change_link_info": "<b>Введите новую реферальную ссылку для {streamer} в {bookmaker} </b>",
}

LEXICON_RU: dict[str, str] = {
    "default_name": "Странник",
    "start": "Привет {username}! \n  Выбери, что ты хочешь сделать. ",
    "yes_referal": "Я уже реферал",
    "no_make_referal": "Стать рефералом",
    "choice_bm": "Рефералом можно быть только"
    " у одного букмерра для одного стримера \n  Выбери букмера",
    "choice_streamer": "Теперь выберети стримера",
    "to_link": "Перейдите по ссылки и зарегистрируйся",
}
