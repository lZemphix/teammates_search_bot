from keyboards import reply, inline
from utils import states
import sqlite3
from data import desc
from data.config import UID
import asyncio
admin_uids = [] 
admin_uids = UID

#Стартовая кнопка
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
    

async def createanc_start(message, database, uid, state):
    await message.answer("Введи свое имя.")
    await state.set_state(states.create_anc.name)

async def createanc_name(message, database, uid, state):
    await state.update_data(name = message.text)
    # await state.set_state(states.create_anc.name)
    await message.answer("Введи свой возраст.")
    await state.set_state(states.create_anc.age)


async def createanc_age(message, database, uid, state):
    await state.update_data(age = message.text)
    await message.answer("Прекрасно! Теперь, двавй определимся с твоим полом. Выбери необходимый вариарнт.", reply_markup = inline.gender())
    await state.set_state(states.create_anc.gender)


async def createanc_gender(callback, database, uid, state):
    await state.update_data(gender = callback.data)    
    await callback.message.delete()
    await callback.message.answer("А теперь укажи, как с тобой можно связаться. Например (Nickname - дискорд)")
    await state.set_state(states.create_anc.connect)

async def createanc_connect(message, database, uid, state):
    await state.update_data(connect = message.text)
    await message.answer("А теперь введи название одной игры, по которой ищешь тиммейтов. Желательно указывать с маленькой буквы и на английском языке")
    await state.set_state(states.create_anc.games)
   
async def createanc_games(message, database, uid, state):
    await state.update_data(games = message.text.lower())
    await message.answer("А теперь, выбери, есть ли у тебя микрофон", reply_markup = inline.micro())
    await state.set_state(states.create_anc.microphone)

async def createanc_microphone(callback, database, uid, state):
    await state.update_data(microphone = callback.data)
    await callback.message.delete()
    await callback.message.answer("Отлично! Теперь напиши подробнее о себе и о своих игровых качествах.")
    await state.set_state(states.create_anc.description)

async def createanc_description(message, uid, state, user_dict, db):
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



async def admin_panel(callback, database):
    if callback.from_user.id in UID:
        await callback.answer(f"""Выберите нужеый вариант""", reply_markup = inline.admin_panel())
    else:
        await callback.answer(f"""Отказано в доступе!""")


async def search_random_user(message, database):
    from random import randint
    database.cursor.execute("SELECT games FROM users WHERE uid = ?", (message.from_user.id,))
    game = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT * FROM users WHERE games = ? AND uid != ? ORDER BY RANDOM() LIMIT 1", (game.lower(), message.from_user.id,))
    random_user = database.cursor.fetchone()
    user_name = random_user[2]
    age = random_user[3]
    gender = random_user[4]
    connect = random_user[5]
    games = random_user[8]
    micro = random_user[6]
    descr = random_user[7]
    await message.answer(f"""📧Анкета пользователя:
                            
    👤Никнейм: {user_name}
    🎂Возраст: {age} лет
    👫Пол: {gender}
    📞Связь: {connect}
    🕹Игра: {games}
    🎤Микрофон: {micro}
    📃Описание: {descr} """)

