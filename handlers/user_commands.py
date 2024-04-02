from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot, BaseMiddleware
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
from utils.dicts import *

router = Router()


# Стартовая панель
@router.message(Command("start"), StateFilter(default_state))
async def start(message: Message):
    await start_message(db, message)

@router.message(Command("donate"))
async def donate(message: Message):
    await message.answer(desc.donate)

# Срабатывает, если пользователь вводит вне машины состояний
@router.message(Command("cancel"), StateFilter(default_state))
async def incorrect_cancel(message: Message, state: FSMContext):
    await message.answer("Отменять нечего!")

# Отмена действия и выход из любой машины состояний
@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_accept(message: Message, state: FSMContext):
    await message.answer("Вы отменили действие!")
    await state.clear()

# Начало создания анкеты и перевод на нужную машину состояний
@router.message(Command("createanc"), StateFilter(default_state))
async def createanc_handler(message: Message, state: FSMContext):
    db.cursor.execute("SELECT description FROM users WHERE uid = ?", (message.from_user.id,))
    desc = db.cursor.fetchone()[0]
    if desc == "none":
        await message.answer("Отлично! Давай начнем с банального. Введи свое имя или никнейм.")
        await state.set_state(create_anc.name)
    else:
        await message.answer("У Вас уже есть анкета. Если вы хотите изменить свою анкету, воспользуйтесь командой /editanc")
        await state.clear()
    
# Проверка на корректность имени и перевод на ввод возраста 
@router.message(StateFilter(create_anc.name))
async def createanc_name_handler(message: Message, state: FSMContext):
    await createanc_name(message, db, message.from_user.id, state)

# Проверка на корректность возраста и перевод на ввод пола
@router.message(StateFilter(create_anc.age), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 100)
async def correct_age_handler(message: Message, state: FSMContext):
    await createanc_age(message, db, message.from_user.id, state)

# Активируется если введен некорректный возраст
@router.message(StateFilter(create_anc.age))
async def incorrect_age(message: Message):
    await message.answer("Введен некорректный возраст! Укажите ваш действительный возраст.")

# Перевод на ввод пола
@router.callback_query(StateFilter(create_anc.gender), F.data.in_(["мужской", "женский", "не опреден"]))
async def correct_gender_handler(callback: CallbackQuery, state: FSMContext):
    await createanc_gender(callback, db, callback.from_user.id, state)

# Активируется если введен некорректный пол
@router.message(StateFilter(create_anc.gender))
async def incorrect_gender(message: Message):
    await message.answer("Используйте кнопки!")
    
@router.message(StateFilter(create_anc.connect))
async def correct_connect_handler(message: Message, state: FSMContext):
    await createanc_connect(message, db, message.from_user.id, state)


@router.callback_query(StateFilter(create_anc.microphone), F.data.in_(["есть", "отсутствует"]))
async def correct_microphone_handler(callback: CallbackQuery, state: FSMContext):
    await createanc_microphone(callback, db, callback.from_user.id, state)

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
async def editanc_handler(message: Message):
    db.cursor.execute("SELECT username FROM users WHERE uid = ?", (message.from_user.id,))
    username = db.cursor.fetchone()[0]
    if username == "unknown":
        await message.answer("У Вас еще нет анкеты, которую можно было бы редактировать! Чтобы создать анкету, воспользуйтесь командой /createanc")
    else:
        await message.answer("Выберите нужное действие", reply_markup = inline.edit_anc())

@router.message(Command("myanc"), StateFilter(default_state))
async def editanc(message: Message):
    db.cursor.execute("SELECT username FROM users WHERE uid = ?", (message.from_user.id,))
    username = db.cursor.fetchone()[0]
    if username == "unknown":
        await message.answer("У Вас еще нет анкеты для просмотра! Чтобы создать анкету, воспользуйтесь командой /createanc")
    else:
        await my_anc(message, db, message.from_user.id)

@router.message(Command("search"))
async def search(message: Message):
    #await callback.message.answer("В разработке")
    await search_random_user(message, db)

@router.message(Command("admin"))
async def admin(message: Message):
    await admin_panel(message, db)

@router.callback_query(F.data.in_("clear_db"))
async def admin(callback: CallbackQuery):
    await db.clear_db(callback, db)

@router.callback_query(F.data.in_("lobby"))
async def admin(callback: CallbackQuery):
    await start_message(callback, db)

@router.callback_query(F.data.in_("add_user"))
async def admin(callback: CallbackQuery):
    await db.add_user(callback)

@router.callback_query(F.data.in_("change_desc"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите новое описание или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.description)
    await callback.message.delete()

@router.message(StateFilter(edit_anc_state.description))
async def edit_ancet_description(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    db.cursor.execute(f"UPDATE users SET description = ? WHERE uid = ?", (message.text, message.from_user.id))
    await message.answer("Описание обновлено!")
    await state.clear()

@router.callback_query(F.data.in_("change_game"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите название игры или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.game)
    await callback.message.delete()

@router.message(StateFilter(edit_anc_state.game))
async def edit_ancet_description(message: Message, state: FSMContext):
    await state.update_data(game = message.text)
    db.cursor.execute("UPDATE users SET games = ? WHERE uid = ?", (message.text.lower(), message.from_user.id))
    db.db.commit()
    db.db.close
    await message.answer("Название игры обновлено!")
    await state.clear()

@router.callback_query(F.data.in_("change_connect"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите новые данные для связи с Вами или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.game)
    await callback.message.delete()


@router.message(StateFilter(edit_anc_state.connect))
async def edit_ancet_description(message: Message, state: FSMContext):
    await state.update_data(connect = message.text)
    db.cursor.execute(f"UPDATE users SET connect = ? WHERE uid = ?", (message.text, message.from_user.id))
    db.db.commit()
    db.db.close
    await message.answer("Данные для связи обновлены!")
    await state.clear()

@router.callback_query(F.data.in_("delete"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    db.cursor.execute("UPDATE users SET username = 'unknown', age = 0, gender = 'unknown', connect = 'none', microphone = 'unknown', description = 'none', games = 'none' WHERE uid = ?", (callback.from_user.id,))
    db.db.commit()
    db.db.close
    await callback.message.answer("Ваша анкета была удалена! Чтобы создать новую, напишите /createanc") 
    await callback.message.delete()

@router.callback_query(F.data.in_("ban"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи айди пользователя, которого хочешь забанить.")
    await state.set_state(ban_state.uid)
    

@router.message(StateFilter(ban_state.uid))
async def edit_ancet_description(message: Message, state: FSMContext):
    await state.update_data(uid = message.text)
    await message.answer("Введи ссрок в днях, на которые необходимо выдать бан.") 
    await state.set_state(ban_state.ban_days)

@router.message(StateFilter(ban_state.ban_days))
async def ban_days_handler(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(ban_days = message.text)
    ban_dict["ban"] = await state.get_data()
    db.cursor.execute(f"UPDATE users SET ban_days = ? WHERE uid = ?", (message.text, ban_dict["ban"]['uid']))
    db.db.commit()
    db.db.close
    await bot.send_message(chat_id=6822091159, text=f"Анкета пользователя с id {ban_dict['ban']['uid']} забанена на {ban_dict['ban']['ban_days']} дней! /admin")
    print(ban_dict) 
    await state.clear()
