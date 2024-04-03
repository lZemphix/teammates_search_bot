from keyboards import inline
from utils import states
import sqlite3
from data import desc
from data.config import UID
import asyncio
admin_uids = [] 
admin_uids = UID

async def start_message(database, message):
    database()
    if database.cursor.execute(f"SELECT * FROM users WHERE uid = {message.from_user.id}").fetchone():
        pass
    else:
        database.cursor.execute(f"INSERT INTO users (uid, username, age, gender, connect, microphone, description, games, active_timer, ban_days) VALUES ({message.from_user.id}, 'unknown', 0, 'unknown', 'unknown', 'unknown','none', 'none', 60, 0)") #number ,uid, username,age, gender, connect, microphone
        #desc, games, active_timer, ban_days 
        database.db.commit()

    database.db.commit()
    database.db.close
    await message.answer(f"""{desc.start(message)}""" )
    

async def createanc_action(message, db, state, create_anc):
    db.cursor.execute("SELECT description FROM users WHERE uid = ?", (message.from_user.id,))
    desc = db.cursor.fetchone()[0]
    if desc == "none":
        await message.answer("Отлично! Давай начнем с банального. Введи свое имя или никнейм.")
        await state.set_state(create_anc.name)
    else:
        await message.answer("У Вас уже есть анкета. Если вы хотите изменить свою анкету, воспользуйтесь командой /editanc")
        await state.clear()

async def editanc_action(message, db):
    db.cursor.execute("SELECT username FROM users WHERE uid = ?", (message.from_user.id,))
    username = db.cursor.fetchone()[0]
    if username == "unknown":
        await message.answer("У Вас еще нет анкеты, которую можно было бы редактировать! Чтобы создать анкету, воспользуйтесь командой /createanc")
    else:
        await message.answer("Выберите нужное действие", reply_markup = inline.edit_anc())

async def myanc_action(message, db):
    db.cursor.execute("SELECT username FROM users WHERE uid = ?", (message.from_user.id,))
    username = db.cursor.fetchone()[0]
    if username == "unknown":
        await message.answer("""У Вас еще нет анкеты для просмотра! Чтобы создать анкету, воспользуйтесь командой 
/createanc""")
    else:
        await my_anc(message, db, message.from_user.id)


async def createanc_start(message, state):
    await message.answer("Введи свое имя.")
    await state.set_state(states.create_anc.name)

async def createanc_name(message, state):
    await state.update_data(name = message.text)
    await message.answer("Введи свой возраст.")
    await state.set_state(states.create_anc.age)


async def createanc_age(message, state):
    await state.update_data(age = message.text)
    await message.answer("Прекрасно! Теперь, двавй определимся с твоим полом. Выбери необходимый вариарнт.", reply_markup = inline.gender())
    await state.set_state(states.create_anc.gender)


async def createanc_gender(callback, state):
    await state.update_data(gender = callback.data)    
    await callback.message.delete()
    await callback.message.answer("А теперь укажи, как с тобой можно связаться. Например (Nickname - дискорд)")
    await state.set_state(states.create_anc.connect)

async def createanc_connect(message, state):
    await state.update_data(connect = message.text)
    await message.answer("А теперь введи название одной игры, по которой ищешь тиммейтов. Желательно указывать с маленькой буквы и на английском языке")
    await state.set_state(states.create_anc.games)
   
async def createanc_games(message, state):
    await state.update_data(games = message.text.lower())
    await message.answer("А теперь, выбери, есть ли у тебя микрофон", reply_markup = inline.micro())
    await state.set_state(states.create_anc.microphone)

async def createanc_microphone(callback, state):
    await state.update_data(microphone = callback.data)
    await callback.message.delete()
    await callback.message.answer("Отлично! Теперь напиши подробнее о себе и о своих игровых качествах.")
    await state.set_state(states.create_anc.description)

async def editanc_description_callback_action(callback, state, edit_anc_state):
    await callback.message.answer("Напишите новое описание или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.description)
    await callback.message.delete()

async def editanc_description_action(db, message, state):
    await state.update_data(description = message.text)
    db.cursor.execute(f"UPDATE users SET description = ? WHERE uid = ?", (message.text, message.from_user.id))
    await message.answer("Описание обновлено!")
    await state.clear()

async def editanc_games_callback_action(callback, state, edit_anc_state):
    await callback.message.answer("Напишите название игры или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.game)
    await callback.message.delete()

async def editanc_game_action(db, message, state):
    await state.update_data(game = message.text)
    db.cursor.execute("UPDATE users SET games = ? WHERE uid = ?", (message.text.lower(), message.from_user.id))
    db.db.commit()
    db.db.close
    await message.answer("Название игры обновлено!")
    await state.clear()

async def editanc_connect_callback_action(callback, state, edit_anc_state):
    await callback.message.answer("Напишите новые данные для связи с Вами или напиши /cancel для отмены редактирования.")
    await state.set_state(edit_anc_state.game)
    await callback.message.delete()

async def editanc_connect_action(db, message, state):
    await state.update_data(connect = message.text)
    db.cursor.execute(f"UPDATE users SET connect = ? WHERE uid = ?", (message.text, message.from_user.id))
    db.db.commit()
    db.db.close
    await message.answer("Данные для связи обновлены!")
    await state.clear()

async def editanc_delete_callback_action(callback, db):
    db.cursor.execute("UPDATE users SET username = 'unknown', age = 0, gender = 'unknown', connect = 'none', microphone = 'unknown', description = 'none', games = 'none' WHERE uid = ?", (callback.from_user.id,))
    db.db.commit()
    db.db.close
    await callback.message.answer("Ваша анкета была удалена! Чтобы создать новую, напишите /createanc") 
    await callback.message.delete()

async def createanc_description(message, state, user_dict, db):
    await state.update_data(description = message.text)
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer("Ваша анкета создана! Теперь можно вести поиск тиммейтов.")
    db.cursor.execute("UPDATE users SET username = ? WHERE uid = ?", ( user_dict[message.from_user.id]['name'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET age = ? WHERE uid = ?", ( user_dict[message.from_user.id]['age'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET gender = ? WHERE uid = ?", ( user_dict[message.from_user.id]['gender'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET connect = ? WHERE uid = ?", ( user_dict[message.from_user.id]['connect'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET microphone = ? WHERE uid = ?", ( user_dict[message.from_user.id]['microphone'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET games = ? WHERE uid = ?", ( user_dict[message.from_user.id]['games'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET description = ? WHERE uid = ?", ( user_dict[message.from_user.id]['description'], message.from_user.id,))
    db.db.commit()

async def my_anc(message, database, uid):
    database.cursor.execute("SELECT username FROM users WHERE uid = ?", (uid,))
    user_name = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT age FROM users WHERE uid = ?", (uid,))
    age = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT gender FROM users WHERE uid = ?", (uid,))
    gender = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT connect FROM users WHERE uid = ?", (uid,))
    connect = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT games FROM users WHERE uid = ?", (uid,))
    games = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT microphone FROM users WHERE uid = ?", (uid,))
    micro = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT description FROM users WHERE uid = ?", (uid,))
    descr = database.cursor.fetchone()[0]
    await message.answer(f"""📧Ваша анкета:
                         
👤Никнейм: {user_name}
🎂Возраст: {age} лет
👫Пол: {gender}
📞Связь: {connect}
🕹Игры: {games}
🎤Микрофон: {micro}
📃Описание: {descr} """)



async def admin_panel(callback):
    if callback.from_user.id in UID:
        await callback.answer(f"""Выберите нужеый вариант""", reply_markup = inline.admin_panel())
    else:
        await callback.answer(f"""Отказано в доступе!""")


async def search_random_user(message, db, uid):
    db.cursor.execute("SELECT games FROM users WHERE uid = ?", (uid,))
    game = db.cursor.fetchone()[0]
    db.cursor.execute("SELECT * FROM users WHERE games = ? AND uid != ? ORDER BY RANDOM() LIMIT 1", (game, uid,))
    random_user = db.cursor.fetchone()
    if random_user is None:
        await message.amswer("К сожалению, не нашлось людей, играющих в данную игру :(")
    else:
        r_uid = random_user[1]
        user_name = random_user[2]
        age = random_user[3]
        gender = random_user[4]
        connect = random_user[5]
        games = random_user[8]
        micro = random_user[6]
        descr = random_user[7]
        msg = await message.answer(f"""📧Анкета пользователя:
                                
👤Никнейм: {user_name}
🎂Возраст: {age} лет
👫Пол: {gender}
📞Связь: {connect}
🕹Игра: {games}
🎤Микрофон: {micro}
📃Описание: {descr} """, reply_markup = inline.search_buttons())
        msg_text = f"""{msg.text} 
        
uid анкеты {r_uid}

uid отправителя {uid}"""
        await message.delete()
        return msg_text
    
async def ban_ancet_callback_action(callback, state, ban_state):
    await callback.message.answer("Введи айди пользователя, которого хочешь забанить.")
    await state.set_state(ban_state.uid)

async def ban_ancet_action(message, state, ban_state):
    await state.update_data(uid = message.text)
    await message.answer("Введи ссрок в днях, на которые необходимо выдать бан.") 
    await state.set_state(ban_state.ban_days)

async def ban_days_action(state, ban_dict, db, message, bot):
    await state.update_data(ban_days = message.text)
    ban_dict["ban"] = await state.get_data()
    db.cursor.execute(f"UPDATE users SET ban_days = ? WHERE uid = ?", (message.text, ban_dict["ban"]['uid']))
    db.db.commit()
    db.db.close
    await message.answer(f"Анкета пользователя с id {ban_dict['ban']['uid']} забанена на {ban_dict['ban']['ban_days']} дней! /admin")
    await bot.send_message(chat_id=6822091159, text=f"""Анкета пользователя с id {ban_dict['ban']['uid']} забанена на {ban_dict['ban']['ban_days']} дней! 
админ: {message.from_user.first_name}
uid {message.from_user.id}""")
    await state.clear()