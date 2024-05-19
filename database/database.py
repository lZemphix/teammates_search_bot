import sqlite3

class database:
    name = "users.db"
    db = sqlite3.connect(name)
    cursor = db.cursor()

    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                number INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER, 
                username TEXT,
                age INTEGER,
                gender TEXT,
                connect TEXT,
                microphone TEXT,
                description TEXT,            
                games TEXT,
                ban_days INTEGER)""")
        self.save()

    async def clear_db(self, callback):
        self.cursor.execute("DELETE FROM users")
        self.cursor.execute(f"INSERT INTO users (uid, username, age, gender, connect, microphone, description, games, active_timer, ban_days) VALUES ({callback.from_user.id}, 'unknown', 0, 'unknown', 'unknown', 'unknown','none', 'none', 60, 0)")
        self.save()

        await callback.message.answer(f"""База данных очищена!""")
        

    async def add_user(self, callback):
        from random import randint
        from random import choice
        games = ['valorant', 'minecraft', 'cs2', 'dota2', 'fortnite', 'gta5', 'lol']
        gender = ['женский', 'мужской', 'не определен']
        new_user = [randint(1000000,9999999), f"name{randint(0, 1000)}", randint(10,40), f"{choice(gender)}", "connect", f"{choice(['есть', 'отсутсвует'])}", f"описание{randint(1,100)}",f"{choice(games)}", 0 ]
        self.cursor.execute(f"INSERT INTO users (uid, username, age, gender, connect, microphone, description, games, ban_days) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(new_user)) 
        self.save()
        await callback.message.answer(f"""Новый пользователь был добавлен!

{new_user}""")
        
    def save(self):
        self.db.commit()
        self.db.close

database().create_db()