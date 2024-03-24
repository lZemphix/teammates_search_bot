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
    gender = InlineKeyboardMarkup(inline_keyboard = [[man, woman, unknown]])
    return gender

def micro():
    yes = InlineKeyboardButton(text = "Да", callback_data="есть")
    no = InlineKeyboardButton(text = "Нет", callback_data="отсутствует")
    microphone = InlineKeyboardMarkup(inline_keyboard = [[yes, no]])
    return microphone

def admin_panel():
    clear_db_button = InlineKeyboardButton(text = "Очистить базу данных", callback_data="clear_db")
    admin_panel = InlineKeyboardMarkup(inline_keyboard = [[clear_db_button]])
    return admin_panel

def lobby():
    lobby_button = InlineKeyboardButton(text = "Главное меню", callback_data="main")
    lobby = InlineKeyboardMarkup(inline_keyboard = [[lobby_button]])
    return lobby