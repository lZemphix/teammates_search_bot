from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

class create_anc(StatesGroup):
    name = State()
    age = State()
    gender = State()
    connect = State()
    games = State()
    microphone = State()
    description = State()
