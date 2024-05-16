from aiogram import Router, F, Bot 
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from database.database import database
from keyboards.inline import *
from aiogram.fsm.context import FSMContext
from utils.dicts import *
from utils.states import *
from data.config import UID
import asyncio
from handlers.user_commands import start_message

admin_uids = UID
admin = Router()

@admin.callback_query(F.data == "admin")
async def admin_panel(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"""Выберите нужеый вариант""", reply_markup = Kb_maker().callback_buttons(["Очистить базу данных", "Добавить пользователя", "Бан пользователя"],["clear_db", "add_user", "ban_user"]))

@admin.callback_query(F.data == "clear_db")
async def clear_database(callback: CallbackQuery):
    await database().clear_db(callback)

@admin.callback_query(F.data == "add_user")
async def add_user(callback: CallbackQuery):
    await database().add_user(callback)

@admin.callback_query(F.data.in_("delete_ancet"), StateFilter(default_state))
async def edit_ancet_delete(callback: CallbackQuery, state: FSMContext):
    database.cursor.execute("UPDATE users SET username = 'unknown', age = 0, gender = 'unknown', connect = 'none', microphone = 'unknown', description = 'none', games = 'none' WHERE uid = ?", (callback.from_user.id,))
    database().save()
    await callback.message.answer("Ваша анкета была удалена!") 
    await callback.message.delete()
    await start_message(callback.message)

@admin.callback_query(F.data == "ban_user", StateFilter(default_state))
async def ban_ancet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи айди пользователя, которого хочешь забанить.")
    await state.set_state(ban_state.uid)
    
@admin.message(StateFilter(ban_state.uid))
async def ban_ancet_state(message: Message, state: FSMContext):
    await state.update_data(uid = message.text)
    await message.answer("Введи ссрок в днях, на которые необходимо выдать бан.") 
    await state.set_state(ban_state.ban_days)

@admin.message(StateFilter(ban_state.ban_days))
async def ban_days_handler(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(ban_days = message.text)
    ban_dict["ban"] = await state.get_data()
    database.cursor.execute(f"UPDATE users SET ban_days = ? WHERE uid = ?", (message.text, ban_dict["ban"]['uid']))
    database().save()
    ban_time_dict[ban_dict["ban"]['uid']] = asyncio.create_task(unban_user(database,ban_time_dict, bot, ban_dict["ban"]['uid']))
    await message.answer(f"Анкета пользователя с id {ban_dict['ban']['uid']} забанена на {ban_dict['ban']['ban_days']} дней!")
    await bot.send_message(chat_id=ban_dict["ban"]['uid'], text=(f"Вы были забанены на {ban_dict['ban']['ban_days']} дней в связи с нарушением правил!"))
    await state.clear()

async def unban_user(database,ban_time_dict, bot, uid):
    ban_days = database.cursor.execute(f"SELECT ban_days FROM users WHERE uid = ?", (uid,)).fetchone()[0]
    await asyncio.sleep(int(ban_days) * 1) #86000 для бана на сутки
    del ban_time_dict[uid]
    database.cursor.execute(f"UPDATE users SET ban_days = 0 WHERE uid = ?", (uid,))
    database().save()
    await bot.send_message(chat_id=uid, text=(f"Вы были разбанены. Старайтесь не нарушать правила, чтобы не получить бан!"))
    await bot.send_message(chat_id=6822091159, text=(f"Анкета пользователя с id {uid} разбанена!"))