from aiogram.fsm.state import State, StatesGroup


class MakeReferalSG(StatesGroup):
    send_link = State()
    check_referal_id = State()
