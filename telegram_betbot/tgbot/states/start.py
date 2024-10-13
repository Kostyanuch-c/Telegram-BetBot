from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()
    choice_bm = State()
    choice_streamer = State()
    send_link = State()
    send_to_check_referal_id = State()
    end_step = State()
