from aiogram.fsm.state import StatesGroup, State


class Choose(StatesGroup):
    choosing_base_curr = State()
    choosing_crypto = State()
