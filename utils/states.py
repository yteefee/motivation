from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    add_quote = State()
    add_tip = State()
    add_challenge = State()
    admin_message = State()

class MoodStates(StatesGroup):
    tracking = State()