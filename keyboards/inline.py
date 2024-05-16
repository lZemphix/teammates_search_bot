from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Kb_maker:
    def __init__(self) -> None:
        self.builder = InlineKeyboardBuilder()

    def callback_buttons(self, titles = None, callbacks = None, rows = 1, main_button = True):
        if titles == None:
            raise ValueError("Parameter 'titles' cannot be empty!")
        elif callbacks == None:
            raise ValueError("Parameter 'callbacks' cannot be empty!")
        elif len(titles) != len(callbacks):
            raise ValueError("'titles' and 'callbacks' lists must be of the same lenght!")
        for title, cd in zip(titles, callbacks):
            self.builder.button(text=title, callback_data=cd)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()
    
    def url_buttons(self, titles = None, urls = None, rows = 1, main_button = True):
        if titles == None:
            raise ValueError("Parameter 'titles' cannot be empty!")
        elif urls == None:
            raise ValueError("Parameter 'urls' cannot be empty!")
        elif len(titles) != len(urls):
            raise ValueError("'titles' and 'urls' lists must be of the same lenght!")
        for title, url in zip(titles, urls):
                self.builder.button(text=title, url=url)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()
    
    def callback_button(self, title = None, callback = None, rows = 1, main_button = True):
        if title == None:
            raise ValueError("Parameter 'titles' cannot be empty!")
        elif callback == None:
            raise ValueError("Parameter 'callbacks' cannot be empty!")
        self.builder.button(text=title, callback_data=callback)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()
    
    def url_button(self, title = None, url = None, rows = 1, main_button = True):
        if title == None:
            raise ValueError("Parameter 'titles' cannot be empty!")
        elif url == None:
            raise ValueError("Parameter 'callbacks' cannot be empty!")
        self.builder.button(text=title, url=url)
        if main_button == True:
            self.builder.button(text="Главное меню", callback_data="main")
        return self.builder.adjust(rows).as_markup()

    def main_button(self):
        self.builder.button(text="Главное меню", callback_data='main')
        return self.builder.as_markup()


# def game_select():
#     cs = InlineKeyboardButton(text = "Counter-Strike 2", callback_data="cs")
#     dota = InlineKeyboardButton(text = "Dota 2", callback_data="dota")
#     lol = InlineKeyboardButton(text = "League of Legends", callback_data="lol")
#     valorant = InlineKeyboardButton(text = "Valorant", callback_data="valorant")
#     minecraft = InlineKeyboardButton(text = "Minecraft", callback_data="minecraft")
#     pubg = InlineKeyboardButton(text = "PUBG", callback_data="pubg")
#     fortnite = InlineKeyboardButton(text = "Fortnite", callback_data="fortnite")
#     apex = InlineKeyboardButton(text = "Apex Legends", callback_data="apex")
#     other = InlineKeyboardButton(text = "Другое", callback_data="other")
#     games = InlineKeyboardMarkup(inline_keyboard = [[cs, dota],
#                                                      [lol, valorant],
#                                                      [minecraft, pubg],
#                                                      [fortnite, apex],
#                                                      [other]])
#     return games

