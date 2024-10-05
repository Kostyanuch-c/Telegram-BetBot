from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    choice_bm = State()
    choice_streamer = State()
    send_link = State()
