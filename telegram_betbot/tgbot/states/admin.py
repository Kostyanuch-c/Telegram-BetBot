from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    start = State()
    choice_bm = State()
    choice_streamer = State()
    main_change = State()
    end_step = State()


class AdminNewsletterSG(StatesGroup):
    choice_bm = State()
    choice_streamer = State()
    create_body_post = State()
    add_photo = State()
    check_newsletter = State()
