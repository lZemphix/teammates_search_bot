from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# О проекте
def links():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Аккаунт", url="tg://resolve?domain=Zemphix"
    )
    builder.button(
        text="Патч-логи", url="https://t.me/+R2OfwWrXc-04OTMy"
    )
    return builder.as_markup()


def gender():
    man = InlineKeyboardButton(text = "Мужской", callback_data="мужской")
    woman = InlineKeyboardButton(text = "Женский", callback_data="женский")
    unknown = InlineKeyboardButton(text = "Не определился", callback_data="не определен")
    gender = InlineKeyboardMarkup(inline_keyboard = [[man, woman], 
                                                     [unknown]])
    return gender

def micro():
    yes = InlineKeyboardButton(text = "Да", callback_data="есть")
    no = InlineKeyboardButton(text = "Нет", callback_data="отсутствует")
    microphone = InlineKeyboardMarkup(inline_keyboard = [[yes, no]])
    return microphone

def admin_panel():
    clear_db_button = InlineKeyboardButton(text = "Очистить базу данных", callback_data="clear_db")
    add_user_button = InlineKeyboardButton(text = "Добавить пользователя", callback_data="add_user")
    ban_user = InlineKeyboardButton(text = "бан пользователя", callback_data="ban")
    admin_panel = InlineKeyboardMarkup(inline_keyboard = [[clear_db_button], 
                                                          [add_user_button],
                                                          [ban_user]])
    return admin_panel

def lobby():
    lobby_button = InlineKeyboardButton(text = "Главное меню", callback_data="main")
    lobby = InlineKeyboardMarkup(inline_keyboard = [[lobby_button]])
    return lobby

def search_buttons():
    next_button = InlineKeyboardButton(text = "Далее", callback_data="next")
    prev_button = InlineKeyboardButton(text = "Главное меню", callback_data="prev")
    report_button = InlineKeyboardButton(text = "Пожаловаться", callback_data="report")
    next = InlineKeyboardMarkup(inline_keyboard = [[next_button],
                                                   [prev_button],
                                                   [report_button]])
    return next

def edit_anc():
    change_desc = InlineKeyboardButton(text = "Изменить описание", callback_data="change_desc")
    change_game = InlineKeyboardButton(text = "Изменить игру", callback_data="change_game")
    change_connect = InlineKeyboardButton(text = "Изменить данные для связи", callback_data="change_connect")
    delete = InlineKeyboardButton(text = "Удалить анкету", callback_data="delete")
    next = InlineKeyboardMarkup(inline_keyboard = [[change_desc],
                                                   [change_game],
                                                   [change_connect],
                                                   [delete]])
    return next

def ban():
    ban_button = InlineKeyboardButton(text = "Забанить", callback_data="ban_ancet")
    ban = InlineKeyboardMarkup(inline_keyboard = [[ban_button]])
    return ban