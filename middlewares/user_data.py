from typing import Awaitable, Callable, Optional, Dict, Any
from aiogram.types import TelegramObject, User
from aiogram import BaseMiddleware
from graphql.mutations import run_update_user
from models import UserModel



class UserDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("event_from_user")
        user_db = await UserModel.get_or_none(uid=user.id)
        if user_db:
            kwargs = {}
            if user_db.first_name != user.first_name:
                kwargs["first_name"] = user.first_name
            if user_db.last_name != user.last_name:
                kwargs["last_name"] = user.last_name
            if user_db.username != user.username:
                kwargs["username"] = user.username
            print(kwargs)
            if len(kwargs.keys()) > 0:
                await run_update_user(user.id, kwargs)
        return await handler(event, data)