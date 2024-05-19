from aiogram import BaseMiddleware
from database.database import database
from aiogram.types import TelegramObject, User
from typing import Callable, Dict, Any, Awaitable
class banMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')
        if user is None:
            pass
        database.cursor.execute("SELECT ban_days FROM users WHERE uid = ?", (user.id,))
        ban_days = database.cursor.fetchone()
        if ban_days is None:
            pass
        else:
            if ban_days[0] > 0:
                return
            else:
                pass
        return await handler(event, data)
