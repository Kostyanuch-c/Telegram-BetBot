LEXICON_COMMANDS: dict[str, str] = {
    "/help": "Список доступных комманд",
    "/info": "Информация о текущих подписках.",
    "/bonus": "Узнать про бонусы",
}

LEXICON_ADMIN: dict[str, str] = {
    "change_link": "Изменить ссылку",
    "change_text": "Изменить текст",
    "change_photo": "Изменить фото",
    "add_photo": "Добавить фото",
    "add_link": "Добавить ссылку",
    "not_need_foto": "Фотография не нужна",
    "not_need_url_button": "Url кнопка не нужна.",
    "newsletter_to_start": "Начать сначала",
    "back": "Назад",
    "make_newsletter": "Cделать рассылку",
    "in_start": "Вернуться в начало",
    "start_admin": (
        "👋 Привет, {username}!\n\n"
        "Добро пожаловать в панель управления!\n"
        "➕ Добавить рефералов — добавить новых пользователей в базу!\n"
        "🔗 Изменить ссылку — обновить реферальную ссылку для стримера!\n"
        "📤 Сделать рассылку — отправить сообщение для определенной группы реферралов.\n\n"
        "Что будем делать первым делом? 😊"
    ),
    "add_referral_keys": "Добавить рефералов",
    "change_streamer_link": "Изменить ссылку",
    "choice_bm": "Выбери букмекера",
    "choice_streamer": "Выбери стримера",
    "add_referral_info": "<b>Введите новые реферральные id для {streamer} в {bookmaker} </b>",
    "change_link_info": "<b>Введите новую реферальную ссылку для {streamer} в {bookmaker} </b>",
    "error_add_referral_or_link": (
        "Вы ввели некорректные данные. Сообщение должно быть строкой, больше одного символа!"
    ),
    "error_wrong_type_input": "Введите, пожалуйста, текстовое сообщение.",
    "success_add_referral": "🎉 Добавление реферальных id стримеру {streamer} "
                            "в {bookmaker} прошло успешно!",
    "success_add_link": "🎉 Изменение реферальной ссылки для стримера {streamer} "
                        "в {bookmaker} прошло успешно!",
    "send_post_body": "<b>Добавление текста!</b>\n\n"
                      "Оправьте основной текст сообщения для рассылки:",
    "send_photo_prompt": "<b>Добавление фотографии!</b>\n\n"
                         "Прикрепите фотографию, если нужно",
    "send_url_text_and_link": (
        "<b>Добавление url кнопки!</b>\n\n"
        "Отправте текст, который будет на кнопке и ссылку <b>через пробел!</b>"
    ),
    "confirmation_prompt": (
        "Вот как будет выглядеть сообщение, которое вы отправите.\n\n"
        "🎯 <b>Целевая аудитория:</b>\n"
        "Рефералы стримера <b>{streamer}</b> из конторы <b>{bookmaker}</b>\n\n"
        "✅ Если вы готовы отправить сообщение, нажмите кнопку <b>'Отправить'</b> для подтверждения."
    ),
    "send_now": "Отправить!",
    "send_success": "Успешно отправлено {successfully_sent} сообщений из {total_messages}",
}
LEXICON_ADMIN_ERRORS: dict[str, str] = {
    "error_invalid_format": (
        "⚠️ Ввод должен содержать текст и ссылку, разделенные пробелом или новой строкой."
    ),
    "error_invalid_button_text": "⚠️ Текст кнопки должен быть длиной не менее 2 символов.",
    "error_is_not_url": "⚠️ Вы отправили не ссылку!\n\n"
                        "Убедитесь, что ссылка начинается с 'http' или 'https'.",
    "error_inout_type_photo": "Отправте, пожалуйста, фото!",
}
LEXICON_RU: dict[str, str] = {
    "default_name": "Странник",
    "start": (
        "👋 Приветствую, {username}!\n\n"
        "Мы рады видеть вас в нашем реферальном проекте! "
        "Вы можете выбрать один из вариантов ниже:\n\n"
        "🔹 <b>Стать рефералом</b> — получите уникальные бонусы и начните свой путь с нами.\n\n"
        "🔹 <b>Я уже реферал</b> — подтвердите свой статус и продолжайте получать бонусы!"
    ),
    "start_pari": (
        "👋 <b>Приветствую, {username}!</b>\n\n"
        "Мы рады видеть вас в нашем реферальном проекте!\n\n"
        "Вы уже являетесь рефералом у букмекера <b>Pari</b> от стримера <b>{streamer_pari}</b>.\n\n"
        "Также у вас есть возможность стать рефералом и у другого букмекера, чтобы "
        "получать еще больше бонусов и преимуществ! 💰\n\n"
        "🔹 <b>Стать рефералом</b> — начните с новым букмекером и получите дополнительные бонусы.\n"
        "🔹 <b>Я уже реферал</b> — подтвердите ваш статус и продолжайте получать бонусы!\n"
        "🔹 <b>{streamer_pari} Up-x</b> — перейти в группу."
    ),
    "start_pari_button": "💼 {streamer_pari} Pari",
    "start_upx": (
        "👋 <b>Приветствую, {username}!</b>\n\n"
        "Мы рады видеть вас в нашем реферальном проекте!\n\n"
        "Вы уже являетесь рефералом у букмекера <b>Up-x</b> от стримера <b>{streamer_upx}</b>.\n\n"
        "Также у вас есть возможность стать рефералом и у другого букмекера, чтобы "
        "получать еще больше бонусов и преимуществ! 💰\n\n"
        "🔹 <b>Стать рефералом</b> — начните с новым букмекером и получите дополнительные бонусы.\n"
        "🔹 <b>Я уже реферал</b> — подтвердите ваш статус и продолжайте получать бонусы!\n"
        "🔹 <b>{streamer_upx} Up-x</b> — перейти в группу."
    ),
    "start_upx_button": "💼 {streamer_upx} Up-x",
    "start_with_all_bm": "🎉 Вы успешно зарегистрировались у всех возможных букмекеров!\n\n"
                         "📲 Ваши ссылки на группы:",
    "yes_referal": "Я уже реферал",
    "no_make_referal": "Стать рефералом",
    "choice_bm": (
        "🎯 <b>Выбери букмекера</b>:\n\n"
        "1. <b>Pari Bet</b> — надёжный букмекер с богатой историей, "
        "предлагающий выгодные коэффициенты на спорт, киберспорт и казино. 📈 "
        "Здесь вас ждут привлекательные акции и бонусы для постоянных игроков.\n\n"
        "2. <b>Up-X</b> — динамично развивающаяся платформа для азартных игр, "
        "с множеством игровых автоматов 🎰, ставок на спорт и моментальных выигрышей. "
        "Быстрые выплаты и регулярные турниры делают её выбором для тех, кто любит адреналин.\n\n"
        "🔍 Выберите одну из опций ниже, чтобы продолжить и указать, "
        "от какого стримера вы реферал.\n\n"
        "⚠️ <b>Рефералом можно быть только у одного букмекера для одного стримера!</b>"
    ),
    "choice_streamer": (
        "Теперь выберите стримера:\n\n"
        "1. <b>Стример 1</b> — опытный и популярный стример, который делится полезными советами "
        "и лайфхаками для ставок на спорт.\n\n"
        "2. <b>Стример 2</b> — специализируется на быстрых играх 🎮 и азарте, "
        "его зрители всегда получают "
        "самые горячие бонусы и акции.\n\n"
        "3. <b>Стример 3</b> — стремительно набирает популярность "
        "благодаря своим уникальным подходам к игре "
        "и интересным турнирам с моментальными выигрышами."
    ),
    "choose_bookmaker_for_referal": (
        "📊 <b>Выберите, в каком букмекере вы являетесь рефералом:</b>\n\n"
        "Нажмите на соответствующую кнопку ниже, чтобы продолжить."
    ),
    "choose_streamer_for_referal": (
        "🎥 <b>Выберите, от какого стримера вы являетесь рефералом:</b>\n\n"
        "Нажмите на соответствуюoщего стримера ниже."
    ),
    "to_link": (
        "🔗 <b>Перейдите по ссылке и зарегистрируйтесь</b> на платформе, чтобы стать рефералом:\n\n"
        "Сообщите как пройдете регистрацию, чтобы продолжить!"
    ),
    "request_id": (
        "🆔 <b>Пожалуйста, отправьте ваш реферальный ID в {bookmaker}</b>, "
        "чтобы мы могли его проверить.\n\n"
        "Убедитесь, что ID введен правильно!"
    ),
    "question_correct": "🕒 <b>Вы уверены, что ввели правильный реферальный ключ?</b>\n\n",
    "waiting_for_confirmation": (
        "🔍 Информация проверяется в нашей базе данных. Пожалуйста, обратите внимание, "
        "что база обновляется раз в день в 00:00.\n\n"
        "Если все данные введены корректно, вам нужно будет подождать до следующего обновления."
    ),
    "confirmation_success": (
        "🎉 <b>Поздравляем!</b> Вы успешно подтвердили свой реферальный статус.\n\n"
        "📲 Теперь вы можете перейти в нашу специальную группу по ссылке ниже "
        "и получать бонусы:\n\n"
        "Или вернитесь в начало и станьте рефералом еще и у другого букмекера, "
        "чтобы получить ещё больше бонусов! 💰"
    ),
}

LEXICON_RU_ERRORS: dict[str, str] = {
    "error_input_referral_id": (
        "Вы ввели некорректные данные."
        " Сообщение должно быть больше одного символа!"
    ),
    "wrong_type_input_referral_id": (
        "Введите, пожалуйста, текстовое сообщение."
    ),
    "choice_not_free_bm": (
        "Вы уже являетесь рефераллом у этого букмеркера"
    ),
    "error_is_not_digit": "ℹ️ Id должен состоять полностью из чисел!",
}
