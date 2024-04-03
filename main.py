import asyncio

from aiogram import Bot, Dispatcher
from data.config import TOKEN
from handlers import user_commands, stated_commands
from utils import middlewares

bot = Bot(TOKEN)
dp = Dispatcher()



async def main():
    dp.include_routers(user_commands.router)
    dp.include_routers(stated_commands.router)
    dp.update.outer_middleware(middlewares.banMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
