from keyboards import reply
from utils import states
import sqlite3
from data import desc

#Стартовая кнопка
async def start_message(database, message):
    database()
    if database.cursor.execute(f"SELECT * FROM users WHERE uid = {message.from_user.id}").fetchone():
        pass
    else:
        database.cursor.execute(f"INSERT INTO users VALUES ({message.from_user.id}, 'unknown', 0, 'unknown', 'unknown', 0,'none', 'none', 15, 0)") #uid, username,age, sex, nickname, microphone
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
    await message.answer("Прекрасно! Теперь, двавй определимся с твоим полом. Выбери необходимый вариарнт.", reply_markup = reply.pol_kb())
    await state.set_state(states.create_anc.sex)


async def createanc_sex(message, database, uid, state):
    await state.update_data(sex = message.text)    
    await message.answer("А теперь вставь ссылку для контакта, чтобы у других была возможность связаться с тобой. Рекомендуется указывать ссылку в формате https:// и желательно, чтобы это был дискорд.")
    await state.set_state(states.create_anc.connect)

async def createanc_connect(message, database, uid, state):
    await state.update_data(connect = message.text)
    await message.answer("А теперь введи назавание игры, (Одной!! в дальнейшем ты можешь поменять ее) для которой хочешь найти тиммейтов. Рекомендуется писать название на английском.")
    await state.set_state(states.create_anc.games)
   
async def createanc_games(message, database, uid, state):
    await state.update_data(games = message.text)
    await message.answer("А теперь, выбери, есть ли у тебя микрофон", reply_markup = reply.micro_kb())
    await state.set_state(states.create_anc.microphone)

async def createanc_microphone(message, database, uid, state):
    await message.answer("Отлично! Теперь напиши подробнее о себе и о своих игровых качествах.")
    await state.update_data(microphone = message.text)
    await state.set_state(states.create_anc.description)

async def createanc_description(message, uid, state, user_dict, db):
    await state.update_data(description = message.text)
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer("Ваша анкета создана! Теперь можно вести поиск тиммейтов.")
    db.cursor.execute("UPDATE users SET username = ? WHERE uid = ?", ( user_dict[message.from_user.id]['name'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET age = ? WHERE uid = ?", ( user_dict[message.from_user.id]['age'], message.from_user.id,))
    db.cursor.execute("UPDATE users SET sex = ? WHERE uid = ?", ( user_dict[message.from_user.id]['sex'], message.from_user.id,))
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
    database.cursor.execute("SELECT sex FROM users WHERE uid = ?", (uid,))
    sex = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT connect FROM users WHERE uid = ?", (uid,))
    connect = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT games FROM users WHERE uid = ?", (uid,))
    games = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT microphone FROM users WHERE uid = ?", (uid,))
    micro = database.cursor.fetchone()[0]
    database.cursor.execute("SELECT description FROM users WHERE uid = ?", (uid,))
    descr = database.cursor.fetchone()[0]
    await message.answer(f"""Моя анкета:
                         
Никнейм: {user_name}
Возраст: {age}
Пол: {sex}
Связь: {connect}
Игры: {games}
Микрофон: {micro}
Описание:{descr} """)








