from typing import Optional
from graphql.mutations import run_get_password_or_create
from models import ApplicationHistory, LifeLocation, UserModel

async def get_user(user_id: int) -> UserModel:
    return await UserModel.get_or_none(uid=user_id)

async def create_user(user_id: int, first_name: str, last_name: Optional[str] = None, username: Optional[str] = None, lang: str = "ru", phone_number: str = None, referrer_id: Optional[int] = None) -> UserModel:
    password = await run_get_password_or_create(user_id, first_name, last_name, username, phone_number, referrer_id)
    return await UserModel.create(uid=user_id, first_name=first_name, last_name=last_name, username=username, password=password, language = lang)

async def add_application_message(uid: int, application_id: int, message_id: int):
    await ApplicationHistory.create(uid=uid, application_id=application_id, message_id=message_id)
    
async def get_applications(application_id: int):
    return await ApplicationHistory.filter(application_id=application_id)

async def add_life_location(message_id: int, user_uid: int):
    return await LifeLocation.create(
        message_id=message_id,
        user_uid=user_uid
    )
    
async def delete_life_location(message_id: int):
    return await LifeLocation.filter(message_id=message_id).delete()

async def delete_life_location_by_user_id(user_id: int):
    return await LifeLocation.filter(user_uid=user_id).delete()

async def get_life_location(message_id: int):
    return await LifeLocation.filter(message_id=message_id).first()