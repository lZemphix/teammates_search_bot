from aiogram.utils.keyboard import InlineKeyboardBuilder

class Kb_maker:
    def __init__(self) -> None:
        self.builder = InlineKeyboardBuilder()

    def callback_buttons(self, titles, callbacks, rows = 1, main_button = True):
        for title, cd in zip(titles, callbacks):
            self.builder.button(text=title, callback_data=cd)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()
    
    def url_buttons(self, titles, urls, rows = 1, main_button = True):
        for title, url in zip(titles, urls):
                self.builder.button(text=title, url=url)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()
    
    def main_button(self):
        self.builder.button(text="Главное меню", callback_data='main')
        return self.builder.as_markup()
    
    def callback_button(self, title, callback, rows = 1, main_button = True):
        self.builder.button(text=title, callback_data=callback)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()
    
    def url_button(self, title, url, rows = 1, main_button = True):
        self.builder.button(text=title, url=url)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()


