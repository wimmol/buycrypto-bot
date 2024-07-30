from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    current_order_id = State()
