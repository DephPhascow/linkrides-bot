from typing import Optional
from graphql.mutations import run_get_password_or_create
from models import UserModel

async def get_user(user_id: int) -> UserModel:
    return await UserModel.get_or_none(uid=user_id)

async def create_user(user_id: int, first_name: str, last_name: Optional[str] = None, username: Optional[str] = None, lang: str = "ru") -> UserModel:
    password = await run_get_password_or_create(user_id, first_name, last_name, username)
    return await UserModel.create(uid=user_id, first_name=first_name, last_name=last_name, username=username, password=password, language = lang)