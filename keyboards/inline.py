from aiogram.utils.keyboard import InlineKeyboardBuilder

class Kb_maker:

    def callback_buttons(self, titles: list, callbacks: list, rows: int = 1, main_button: bool = True):
        builder = InlineKeyboardBuilder()
        for title, cd in zip(titles, callbacks):
            builder.button(text=title, callback_data=cd)
        if main_button == True:
            builder.button(text="Главное меню", callback_data="main")
        return builder.adjust(rows).as_markup()
    
    def url_buttons(self, titles: list, urls: list, rows: int = 1, main_button: bool = True):
        builder = InlineKeyboardBuilder()
        for title, url in zip(titles, urls):
                builder.button(text=title, url=url)
        if main_button == True:
            builder.button(text="Главное меню", callback_data="main")
        return builder.adjust(rows).as_markup()
    
    def main_button(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="Главное меню", callback_data='main')
        return builder.as_markup()
    
    def callback_button(self, title: str, callback: str, rows: int = 1, main_button: bool = True):
        builder = InlineKeyboardBuilder()
        builder.button(text=title, callback_data=callback)
        if main_button == True:
            builder.button(text="Главное меню", callback_data="main")
        return builder.adjust(rows).as_markup()
    
    def url_button(self, title: str, url: str, rows: int = 1, main_button: bool = True):
        builder = InlineKeyboardBuilder()
        builder.button(text=title, url=url)
        if main_button == True:
            builder.button(text="Главное меню", callback_data="main")
        return builder.adjust(rows).as_markup()


