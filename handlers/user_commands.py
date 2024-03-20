from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram import Bot
from database.database import database as db
from handlers.actions import *
from keyboards import reply, inline
from data import desc
from handlers.actions import *
from utils.states import *
from keyboards import reply
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3


router = Router()
user_dict: dict[int, dict[str, str | int | bool]] = {}  


# Стартовая панель
@router.message(Command("start"), StateFilter(default_state))
async def start(message: Message):
    await start_message(db, message)

# Срабатывает, если пользователь вводит вне машины состояний
@router.message(Command("cancel"), StateFilter(default_state))
async def incorrect_cancel(message: Message, state: FSMContext):
    await message.answer("Отменять нечего!")

# Отмена действия и выход из любой машины состояний
@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_accept(message: Message, state: FSMContext):
    await message.answer("Вы отменили создание анкеты!")
    await state.clear()

# Начало создания анкеты и перевод на нужную машину состояний
@router.message(Command("createanc"), StateFilter(default_state))
async def createanc_handler(message: Message, state: FSMContext):
    await message.answer("Отлично! Давай начнем с банального. Введи свое имя или никнейм.")
    await state.set_state(create_anc.name)
    
# Проверка на корректность имени и перевод на ввод возраста 
@router.message(StateFilter(create_anc.name), F.text.isalpha())
async def createanc_name_handler(message: Message, state: FSMContext):
    await createanc_name(message, db, message.from_user.id, state)

# если имя некорректное
@router.message(StateFilter(create_anc.name))
async def incorrect_name(message: Message):
    await message.answer("Введено некорректное имя!")  

# Проверка на корректность возраста и перевод на ввод пола
@router.message(StateFilter(create_anc.age), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 100)
async def correct_age_handler(message: Message, state: FSMContext):
    await createanc_age(message, db, message.from_user.id, state)

# Активируется если введен некорректный возраст
@router.message(StateFilter(create_anc.age))
async def incorrect_age(message: Message):
    await message.answer("Введен некорректный возраст! Укажите ваш действительный возраст.")

# Перевод на ввод пола
@router.message(StateFilter(create_anc.sex))
async def correct_sex_handler(message: Message, state: FSMContext):
    await createanc_sex(message, db, message.from_user.id, state)



# Активируется если введен некорректный пол
@router.message(StateFilter(create_anc.sex))
async def incorrect_sex(message: Message):
    await message.answer("Введен некорректный пол!")
    
@router.message(StateFilter(create_anc.connect))
async def correct_connect_handler(message: Message, state: FSMContext):
    await createanc_connect(message, db, message.from_user.id, state)


@router.message(StateFilter(create_anc.microphone))
async def correct_microphone_handler(message: Message, state: FSMContext):
    await createanc_microphone(message, db, message.from_user.id, state)



@router.message(StateFilter(create_anc.games))
async def correct_games_handler(message: Message, state: FSMContext):
    await createanc_games(message, db, message.from_user.id, state)


@router.message(StateFilter(create_anc.description))
async def correct_description_handler(message: Message, state: FSMContext):
    await createanc_description(message, message.from_user.id, state, user_dict, db)

 
# Помощь
@router.message(Command("help"), StateFilter(default_state))
async def help(message: Message):
    await message.answer(desc.help)


@router.message(Command("rules"), StateFilter(default_state))
async def rules(message: Message):
    await message.answer(desc.rules)
                

@router.message(Command("editanc"), StateFilter(default_state))
async def editanc(message: Message):
    await message.answer("В разработке")

@router.message(Command("myanc"), StateFilter(default_state))
async def editanc(message: Message):
    await my_anc(message, db, message.from_user.id)

@router.message(Command("search"))
async def search(message: Message):
    await message.answer("В разработке")
    # await search_message(db, message)