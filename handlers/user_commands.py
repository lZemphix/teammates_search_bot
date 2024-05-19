from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from database.database import database
from keyboards.inline import *
from aiogram.fsm.context import FSMContext
from utils.dicts import *
from utils.states import *
from data import desc
from data.config import UID

admin_uids = UID
router = Router()

@router.message(Command("start"), StateFilter(default_state))
async def start_message(message: Message):
    database().create_db()
    user_exists = database.cursor.execute(f"SELECT * FROM users WHERE uid = {message.from_user.id}").fetchone()
    if user_exists:
        pass
    else:
        database.cursor.execute(f"INSERT INTO users (uid, username, age, gender, connect, microphone, description, games, ban_days) VALUES ({message.from_user.id}, 'unknown', 0, 'unknown', 'unknown', 'unknown','none', 'none', 0)")
    database().save()
    
    buttons, callbacks = ['📃 Анкета', '❗ Правила', '❓ Помощь', '🔎 Поиск'],['ancet', 'rules', 'help', 'search']
    
    if message.from_user.id in admin_uids:
        buttons.append('⚙ Админ панель')
        callbacks.append('admin')
    
    await message.answer(f"""Привет, {message.from_user.first_name}! Я помогу тебе найти тиммейта на одну катку или друзей для любой игры. Выбери интересующий тебя пункт.""", reply_markup=Kb_maker().callback_buttons(titles=buttons, callbacks=callbacks, rows=2))

@router.callback_query(F.data == 'rules')
async def rules(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(desc.rules, reply_markup=Kb_maker().main_button())

@router.callback_query(F.data == 'donate')
async def donate(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(desc.donate, reply_markup=Kb_maker().main_button())
              
@router.callback_query(F.data == 'help')
async def help(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(desc.help, reply_markup=Kb_maker().callback_button('💲 Донат', 'donate'))


@router.callback_query(F.data == ("edit_anc"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выберите нужное действие", reply_markup = Kb_maker().callback_buttons(
        titles=["Изменить описание", "Изменить игру", "Изменить данные для связи", "Удалить анкету"],
        callbacks=["change_desc", "change_game", "change_connect", "delete_ancet"]))

@router.callback_query(F.data == "ancet")
async def editanc(callback: CallbackQuery):
    await callback.message.delete()
    username = database.cursor.execute("SELECT username FROM users WHERE uid = ?", (callback.from_user.id,)).fetchone()[0]
    if username == "unknown":
        await callback.message.answer("У Вас еще нет анкеты! Чтобы создать анкету нажмите на '📃 Создать анкету' ",  reply_markup=Kb_maker().callback_button('📃 Создать анкету','create_anc'))
    else:
        user_data = database.cursor.execute("SELECT * FROM users WHERE uid = ?", (callback.from_user.id,)).fetchone()
        await callback.message.answer(f"""📧Ваша анкета:
                         
👤Никнейм: {user_data[2]}
🎂Возраст: {user_data[3]} лет
👫Пол: {user_data[4]}
📞Связь: {user_data[5]}
🕹Игра: {user_data[8]}
🎤Микрофон: {user_data[6]}
📃Описание: {user_data[7]} """, reply_markup=Kb_maker().callback_button('Редактировать анкету', 'edit_anc'))
        database().save()

@router.callback_query(F.data == "search")
async def search(callback: CallbackQuery):
    game = database.cursor.execute("SELECT games FROM users WHERE uid = ?", (callback.from_user.id,)).fetchone()[0]
    if game == "none":
        callback.message.delete()
        await callback.message.answer("У Вас еще нет анкеты! Чтобы создать анкету нажмите на '📃 Создать анкету' ",  reply_markup=Kb_maker().callback_button('📃 Создать анкету','create_anc'))
    else:
        try:
            random_user = database.cursor.execute("SELECT * FROM users WHERE games = ? AND uid != ? ORDER BY RANDOM() LIMIT 1", (game, callback.from_user.id,)).fetchone()
            if random_user:
                await callback.message.answer(f"""📧Анкета пользователя:
                                                                            
👤Никнейм: {random_user[2]}
🎂Возраст: {random_user[3]} лет
👫Пол: {random_user[4]}
📞Связь: {random_user[5]}
🕹Игра: {random_user[8]}
🎤Микрофон: {random_user[6]}
📃Описание: {random_user[7]} """, reply_markup = Kb_maker().callback_buttons(["Далее", "Пожаловаться"], ["search",str(random_user[1])]))
                await callback.message.delete()
                database().save()
            else:
                await callback.message.answer("К сожалению, не нашлось людей, играющих в данную игру :(")

        except TypeError:
            await callback.message.answer("К сожалению, не нашлось людей, играющих в данную игру :(") 
            # print("NoneType error")

@router.callback_query(F.data == "main")
async def main(callback: CallbackQuery):
    await callback.message.delete()
    database().create_db()
    if database.cursor.execute(f"SELECT * FROM users WHERE uid = {callback.from_user.id}").fetchone():
        pass
    else:
        database.cursor.execute(f"INSERT INTO users (uid, username, age, gender, connect, microphone, description, games, ban_days) VALUES ({callback.from_user.id}, 'unknown', 0, 'unknown', 'unknown', 'unknown','none', 'none', 0)")  
    buttons, callbacks = ["📃 Анкета", "❗ Правила", "❓ Помощь", "🔎 Поиск"], ['ancet', 'rules', 'help', 'search']
    if callback.from_user.id in admin_uids:
        buttons.append('⚙ Админ панель')
        callbacks.append('admin')
    
    await callback.message.answer(f"""Привет, {callback.from_user.first_name}! Я помогу тебе найти тиммейта на одну катку или друзей для любой игры. Выбери интересующий тебя пункт.""", reply_markup=Kb_maker().callback_buttons(titles=buttons, callbacks=callbacks, rows=2))

@router.callback_query(F.data.regexp(r"^(\d+)$").as_("uid"))
async def report_system(callback: CallbackQuery, bot: Bot, uid: int):
        database.cursor.execute("SELECT * FROM users WHERE uid = ?", (uid[0],))
        random_user_data = database.cursor.fetchone()
        database().save()
        await bot.send_message(chat_id =admin_uids[0], text = f"""📧Анкета пользователя:
                         
👤Никнейм: {random_user_data[2]}
🎂Возраст: {random_user_data[3]} лет
👫Пол: {random_user_data[4]}
📞Связь: {random_user_data[5]}
🕹Игра: {random_user_data[8]}
🎤Микрофон: {random_user_data[6]}
📃Описание: {random_user_data[7]} 

uid: `{uid[0]}`""", parse_mode='MARKDOWN', reply_markup=Kb_maker().callback_button('Забанить', 'ban_user'))
        await callback.message.answer("Жалоба отправлена!")
        await search(callback)
        
@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_accept(message: Message, state: FSMContext):
    await message.answer("Вы отменили действие!")
    await state.clear()
    await start_message(message)
    
@router.message(Command("cancel"))
async def incorrect_cancel(message: Message):
    await message.answer("Отменять нечего!")

@router.callback_query(F.data == 'create_anc', StateFilter(default_state))
async def createanc(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отлично! Давай начнем с банального. Введи свое имя или никнейм.")
    await state.set_state(create_anc.name)
 
@router.message(StateFilter(create_anc.name))
async def createanc_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Введи свой возраст.")
    await state.set_state(create_anc.age)

@router.message(StateFilter(create_anc.age), lambda x: x.text.isdigit() and 6 <= int(x.text) <= 100)
async def correct_age(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Прекрасно! Теперь, двавй определимся с твоим полом. Выбери необходимый вариарнт.", reply_markup = Kb_maker().callback_buttons(["мужской", "женский", "не опреден"],["мужской", "женский", "не опреден"], main_button=False))
    await state.set_state(create_anc.gender)

@router.message(StateFilter(create_anc.age))
async def incorrect_age(message: Message):
    await message.answer("Введен некорректный возраст! Укажите ваш действительный возраст.")

@router.callback_query(StateFilter(create_anc.gender), F.data.in_(["мужской", "женский", "не опреден"]))
async def correct_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender = callback.data)    
    await callback.message.delete()
    await callback.message.answer("А теперь укажи, как с тобой можно связаться. Например 'Nickname - дискорд' или '@username - телеграм'")
    await state.set_state(create_anc.connect)

@router.message(StateFilter(create_anc.gender))
async def incorrect_gender(message: Message):
    await message.answer("Используйте кнопки!")
    
@router.message(StateFilter(create_anc.connect))
async def correct_connect(message: Message, state: FSMContext):
    await state.update_data(connect = message.text)
    await message.answer("Напиши название игры. Например Minecraft, Dota 2 и тд.(желательно на английском и только одну игру).")
    await state.set_state(create_anc.games)

@router.message(StateFilter(create_anc.games))
async def correct_games(message: Message, state: FSMContext):
    await state.update_data(games = message.text.lower())
    await message.answer("А теперь, выбери, есть ли у тебя микрофон", reply_markup = Kb_maker().callback_buttons(["есть", "отсутствует"], ["есть", "отсутствует"], main_button=False))
    await state.set_state(create_anc.microphone)

@router.callback_query(StateFilter(create_anc.microphone), F.data.in_(["есть", "отсутствует"]))
async def correct_microphone(callback: CallbackQuery, state: FSMContext):
    await state.update_data(microphone = callback.data)
    await callback.message.delete()
    await callback.message.answer("Отлично! Теперь напиши подробнее о себе и о своих игровых качествах.")
    await state.set_state(create_anc.description)


@router.message(StateFilter(create_anc.description))
async def correct_description(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    uid = message.from_user.id
    user_dict[uid] = await state.get_data()
    await state.clear()
    await message.answer("Ваша анкета создана! Теперь можно вести поиск тиммейтов.")
    database.cursor.execute("UPDATE users SET username = ? WHERE uid = ?", ( user_dict[uid]['name'], uid,))
    database.cursor.execute("UPDATE users SET age = ? WHERE uid = ?", ( user_dict[uid]['age'], uid,))
    database.cursor.execute("UPDATE users SET gender = ? WHERE uid = ?", ( user_dict[uid]['gender'], uid,))
    database.cursor.execute("UPDATE users SET connect = ? WHERE uid = ?", ( user_dict[uid]['connect'], uid,))
    database.cursor.execute("UPDATE users SET microphone = ? WHERE uid = ?", ( user_dict[uid]['microphone'], uid,))
    database.cursor.execute("UPDATE users SET games = ? WHERE uid = ?", ( ((user_dict[uid]['games']).lower()).replace(" ", ""), uid,))
    database.cursor.execute("UPDATE users SET description = ? WHERE uid = ?", ( user_dict[uid]['description'], uid,))
    database().save()
    await start_message(message)

@router.callback_query(F.data.in_("change_desc"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите новое описание или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.description)
    await callback.message.delete()

@router.message(StateFilter(edit_anc_state.description))
async def edit_ancet_description(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    database.cursor.execute(f"UPDATE users SET description = ? WHERE uid = ?", (message.text, message.from_user.id))
    database().save()
    await message.answer("Описание обновлено!")
    await start_message(message)
    await state.clear()

@router.callback_query(F.data.in_("change_game"), StateFilter(default_state))
async def edit_ancet_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напиши название игры или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.game)
    await callback.message.delete()

@router.message(StateFilter(edit_anc_state.game))
async def edit_ancet_game(message: Message, state: FSMContext):
    await state.update_data(game = message.text)
    database.cursor.execute("UPDATE users SET games = ? WHERE uid = ?", (message.text.lower().replace(" ", ""), message.from_user.id))
    database().save()
    await message.answer("Название игры обновлено!")
    await state.clear()
    await start_message(message)


@router.callback_query(F.data.in_("change_connect"), StateFilter(default_state))
async def edit_ancet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите новые данные для связи с Вами или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.connect)
    await callback.message.delete()


@router.message(StateFilter(edit_anc_state.connect))
async def edit_ancet_connect(message: Message, state: FSMContext):
    await state.update_data(connect = message.text)
    database.cursor.execute(f"UPDATE users SET connect = ? WHERE uid = ?", (message.text, message.from_user.id))
    database().save()
    await message.answer("Данные для связи обновлены!")
    await state.clear()
    await start_message(message)
