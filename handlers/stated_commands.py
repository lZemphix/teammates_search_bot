from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from database.database import database as db
from handlers.actions import *
from keyboards import reply, inline
from utils.states import *
from aiogram.fsm.context import FSMContext
from utils.dicts import *

router = Router()

@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_accept(message: Message, state: FSMContext):
    await message.answer("Вы отменили действие!")
    await state.clear()
    
@router.message(Command("cancel"))
async def incorrect_cancel(message: Message, state: FSMContext):
    await message.answer("Отменять нечего!")

# Отмена действия и выход из любой машины состояний

# Начало создания анкеты и перевод на нужную машину состояний
@router.message(Command("createanc"), StateFilter(default_state))
async def createanc_handler(message: Message, state: FSMContext):
    await createanc_action(message, db, state, create_anc)
    
# Проверка на корректность имени и перевод на ввод возраста 
@router.message(StateFilter(create_anc.name))
async def createanc_name_handler(message: Message, state: FSMContext):
    await createanc_name(message, state)

# Проверка на корректность возраста и перевод на ввод пола
@router.message(StateFilter(create_anc.age), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 100)
async def correct_age_handler(message: Message, state: FSMContext):
    await createanc_age(message, state)

# Активируется если введен некорректный возраст
@router.message(StateFilter(create_anc.age))
async def incorrect_age(message: Message):
    await message.answer("Введен некорректный возраст! Укажите ваш действительный возраст.")

# Перевод на ввод пола
@router.callback_query(StateFilter(create_anc.gender), F.data.in_(["мужской", "женский", "не опреден"]))
async def correct_gender_handler(callback: CallbackQuery, state: FSMContext):
    await createanc_gender(callback, state)

# Активируется если введен некорректный пол
@router.message(StateFilter(create_anc.gender))
async def incorrect_gender(message: Message):
    await message.answer("Используйте кнопки!")
    
@router.message(StateFilter(create_anc.connect))
async def correct_connect_handler(message: Message, state: FSMContext):
    await createanc_connect(message, state)


@router.callback_query(StateFilter(create_anc.microphone), F.data.in_(["есть", "отсутствует"]))
async def correct_microphone_handler(callback: CallbackQuery, state: FSMContext):
    await createanc_microphone(callback, state)

@router.message(StateFilter(create_anc.games))
async def correct_games_handler(message: Message, state: FSMContext):
    await createanc_games(message, state)


@router.message(StateFilter(create_anc.description))
async def correct_description_handler(message: Message, state: FSMContext):
    await createanc_description(message, state, user_dict, db)

@router.callback_query(F.data.in_("change_desc"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await editanc_description_callback_action(callback, state, edit_anc_state)

@router.message(StateFilter(edit_anc_state.description))
async def edit_ancet_description(message: Message, state: FSMContext):
    await editanc_description_action(db, message, state)

@router.callback_query(F.data.in_("change_game"), StateFilter(default_state))
async def edit_ancet_callback(callback: CallbackQuery, state: FSMContext):
    await editanc_games_callback_action(callback, state, edit_anc_state)

@router.message(StateFilter(edit_anc_state.game))
async def edit_ancet_game(message: Message, state: FSMContext):
    await editanc_game_action(db, message, state)

@router.callback_query(F.data.in_("change_connect"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await editanc_connect_callback_action(callback, state, edit_anc_state)


@router.message(StateFilter(edit_anc_state.connect))
async def edit_ancet_connect(message: Message, state: FSMContext):
    await editanc_connect_action(db, message, state)

@router.callback_query(F.data.in_("delete"), StateFilter(default_state))
async def edit_ancet_delete(callback: CallbackQuery, state: FSMContext):
    await editanc_delete_callback_action(callback, db)

@router.callback_query(F.data.in_("ban"), StateFilter(default_state))
async def ban_ancet(callback: CallbackQuery, state: FSMContext):
    await ban_ancet_callback_action(callback, state, ban_state)
    
@router.message(StateFilter(ban_state.uid))
async def ban_ancet_state(message: Message, state: FSMContext):
    await ban_ancet_action(message, state, ban_state)

@router.message(StateFilter(ban_state.ban_days))
async def ban_days_handler(message: Message, state: FSMContext, bot: Bot):
    await ban_days_action(state, ban_dict, db, message, bot, ban_time_dict)
