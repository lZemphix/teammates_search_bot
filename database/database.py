import sqlite3

class database():
    name = "users.db"
    db = sqlite3.connect(name)
    cursor = db.cursor()

    def __init__(self):
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
                active_timer INTEGER,
                ban_days INTEGER)""")
        self.db.commit()
        self.db.close
    @staticmethod
    async def clear_db(self,callback):
        self.cursor.execute("DELETE FROM users")
        self.db.commit()
        await callback.message.answer(f"""База данных очищена!""")
        
    @staticmethod
    async def add_user(callback):
        from random import randint
        new_user = [randint(1000000,9999999), f"name{randint(0, 1000)}", randint(10,40), "мужской", "connect", "есть", f"описание{randint(1,100)}","valorant", 15, 0 ]
        database.cursor.execute(f"INSERT INTO users (uid, username, age, gender, connect, microphone, description, games, active_timer, ban_days) VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?)",(new_user)) 
        #number ,uid, username,age, gender, connect, microphone, description, games, active_timer, ban_days 
        database.db.commit()
        await callback.message.answer(f"""Новый пользователь был добавлен!""")
        
    
            

    
