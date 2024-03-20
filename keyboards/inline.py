from aiogram.utils.keyboard import InlineKeyboardBuilder

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

def pol():
    builder = InlineKeyboardBuilder()
    builder.button(text = "Деушка", callback_data="woman")
    builder.button(text = "Мужшина", callback_data="man")
    return builder.as_markup()
