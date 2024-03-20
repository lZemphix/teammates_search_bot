import sqlite3

class database():
    name = "users.db"
    db = sqlite3.connect(name)
    cursor = db.cursor()

    def __init__(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                uid INTEGER, 
                username TEXT,
                age INTEGER,
                sex TEXT,
                connect TEXT,
                microphone TEXT,
                description TEXT,            
                games TEXT,
                active_timer INTEGER,
                ban_days INTEGER)""")
        self.db.commit()
        self.db.close


        

            

    
