import asyncio, pathlib, os

from aiogram import Bot, Dispatcher
from handlers import user_commands, admin_commands
from utils import middlewares
from dotenv import load_dotenv

dotenv_path = pathlib.Path('data/.env')
load_dotenv(dotenv_path=dotenv_path)

bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()



async def main():
    dp.include_routers(user_commands.router, admin_commands.admin)
    dp.update.outer_middleware(middlewares.banMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("Bot was stoped!")
