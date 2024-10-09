from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()
    choice_bm = State()
    choice_streamer = State()
    send_link = State()
    check_referal_id = State()
    end_check = State()
