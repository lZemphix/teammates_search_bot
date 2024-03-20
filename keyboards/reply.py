from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Главное меню
def pol_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Мужской")
    builder.button(text="Женский")
    builder.button(text="Не определился")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard = True)

def micro_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="есть")
    builder.button(text="нет")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard = True, one_time_keyboard = True)