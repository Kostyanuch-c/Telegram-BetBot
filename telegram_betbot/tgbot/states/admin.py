from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    start = State()


class AdminChoiceBmAndStreamer(StatesGroup):
    choice_bm = State()
    choice_streamer = State()


class AdminConfirmRefs(StatesGroup):
    send_confirms = State()
    end_confirms = State()


class AdminChangeRefsLink(StatesGroup):
    send_link = State()
    end_change_link = State()


class AdminNewsletterSG(StatesGroup):
    add_text_body_post = State()
    add_photo = State()
    add_url_button = State()
    check_newsletter = State()
    end_send_newsletter = State()
