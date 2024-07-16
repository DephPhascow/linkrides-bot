from typing import Awaitable, Callable, Optional, Dict, Any

from aiogram.types import TelegramObject, User
from aiogram import BaseMiddleware, Bot



class UserDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("event_from_user")
        bot: Bot = data.get("bot")

        return await handler(event, data)