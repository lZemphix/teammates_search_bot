import sqlite3
from aiogram import Bot, Dispatcher
from data.config import TOKEN

uid = int()
nickname = ""
bot = Bot(TOKEN)
dp = Dispatcher()
db = sqlite3.connect("users.db")
cursor = db.cursor()


def choice_action(uid, nickname):
    print ("""Выберите действие: 
           1. Обновить ежедневный бонус
           2. Пополнить баланс
           3. Добавить премиум
           """)
    action = int(input())
    if action == 1:
        set_daily(uid, nickname)
    elif action == 2:
        add_balance(uid, nickname)
    elif action == 3:
        add_premium(uid, nickname)    

def sign_in():
    account = int(input("""Выберите аккаунт:
    1. secret
    2. zemphix 
    3. kimoshi
    4. Другой аккаунт 
    5. Отмена 
                        """))
    if account == 1:
        uid = 1162852333
        nickname = "secret"
        choice_action(uid)
        return uid, nickname
    elif account == 2:
        uid = 948505838
        nickname = "zemphix"
        choice_action(uid)
        return uid, nickname
    elif account == 3:
        uid = 6568267175
        nickname = "kimoshi"
        choice_action(uid, nickname)
        return uid, nickname
    elif account == 4:
        uid = int(input("Введите uid пользователя: "))
        nickname = f"пользователя с uid: {uid}"
        choice_action(uid, nickname)
        return uid, nickname
    elif account == 5:
        print ("Отменено.")

def set_daily(uid , nickname):
    cursor.execute("UPDATE users SET daily = 1 WHERE uid = ? ", (uid,))
    db.commit()
    db.close
    print(f"Ежедннвный бонус обновлен для {nickname}.")
    sign_in()

def add_balance(uid, nickname):
    balance = input("Введите количесво: ")
    cursor.execute("UPDATE users SET balance = balance + ? WHERE uid = ? ", (balance, uid))
    db.commit()
    db.close
    print(f"На баланс {nickname} зачисленно {balance} 🎫.")
    sign_in()

def add_premium(uid, nickname):
    premium = input("Введите количество дней: ")
    cursor.execute("UPDATE users SET premium = premium + ? WHERE uid = ? ", (premium, uid))
    db.commit()
    db.close
    print(f"На аккаунт {nickname} зачисленно {premium} 👑.")
    sign_in()


sign_in()