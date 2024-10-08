from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    start = State()
    choice_bm = State()
    choice_streamer = State()
    main_change = State()
    end_step = State()
