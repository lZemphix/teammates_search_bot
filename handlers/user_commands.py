from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from database.database import database as db
from handlers.actions import *
from keyboards import reply, inline
from data import desc
from handlers.actions import *
from utils.states import *
from utils.dicts import *

router = Router()

# Стартовая панель
@router.message(Command("start"), StateFilter(default_state))
async def start(message: Message):
    await start_message(db, message)

@router.message(Command("donate"))
async def donate(message: Message):
    await message.answer(desc.donate)


@router.message(Command("rules"))
async def rules(message: Message):
    await message.answer(desc.rules)
                
@router.message(Command("help"))
async def help(message: Message):
    await message.answer(desc.help)

@router.message(Command("editanc"), StateFilter(default_state))
async def editanc_handler(message: Message):
    await editanc_action(message, db)

@router.message(Command("myanc"))
async def editanc(message: Message):
    await myanc_action(message, db)

@router.message(Command("search"))
async def search(message: Message):
    await search_random_user(message, db, message.from_user.id)

@router.callback_query(F.data.in_("next"))
async def search(callback: CallbackQuery):
    await search_random_user(callback.message, db, callback.from_user.id)

@router.callback_query(F.data.in_("prev"))
async def search(callback: CallbackQuery):
    await callback.message.delete()
    await start_message(db, callback.message)

@router.message(Command("admin"))
async def admin(message: Message):
    await admin_panel(message)

@router.callback_query(F.data.in_("clear_db"))
async def admin(callback: CallbackQuery):
    await db.clear_db(callback)

@router.callback_query(F.data.in_("lobby"))
async def admin(callback: CallbackQuery):
    await start_message(callback, db)

@router.callback_query(F.data.in_("add_user"))
async def admin(callback: CallbackQuery):
    await db.add_user(callback)

@router.callback_query(F.data.in_("report"))
async def report_system(callback: CallbackQuery, bot: Bot):
    await report_system_callback_action(callback, bot, db)