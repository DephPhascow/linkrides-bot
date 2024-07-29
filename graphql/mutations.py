from typing import Optional, Dict

from graphql.m_types import DrivingStatus
from models import UserModel

from .core.middlewares.auth_middleware import AuthMiddleware
from .core.utils import gen_mutate
from .settings import gql

def get_password():
    return gen_mutate(
        name="getPasswordOrCreate",
        var={
            "tgId": "String!",
            "firstName": "String",
            "lastName": "String",
            "username": "String",
        }
    )
    
def update_user():
    return gen_mutate(
        name="updateUser",
        request="id",
        q_words="data.updateUser.id",
        var={
            "firstName": "String",
            "lastName": "String",
            "username": "String",
        }
    )
def taxi_set_my_location():
    return gen_mutate(
        name="taxiSetMyCurrentLocation",
        request="__typename",
        var={
            "latitude": "Float!",
            "longitude": "Float!",
            "status": "DrivingStatus",
        }
    )
def taxi_set_status():
    return gen_mutate(
        name="taxiSetStatus",
        request="__typename",
        var={
            "status": "DrivingStatus!",
        }
    )
    
async def run_taxi_set_status(tg_id: int, status: DrivingStatus) -> int:
    executor = gql.add_query("taxi_set_status", taxi_set_status())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    response = await executor.execute(variables={
        "status": status
    })
    return response['taxiSetStatus']

async def run_taxi_set_my_location(tg_id: int, latitude: float, longitude: float, status: DrivingStatus) -> int:
    executor = gql.add_query("taxiSetMyCurrentLocation", taxi_set_my_location())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    response = await executor.execute(variables={
        "latitude": latitude,
        "longitude": longitude,
        "status": status
    })
    return response['taxiSetMyCurrentLocation']

async def run_get_password_or_create(tg_id: int, first_name: str, last_name: Optional[str] = None, username: Optional[str] = None) -> str:
    executor = gql.add_query("getPasswordOrCreate", get_password())
    response = await executor.execute(variables={
        "tgId": f'{tg_id}',
        "firstName": first_name,
        "lastName": last_name,
        "username": username
    }, ignore_middlewares=['auth'])
    return response['getPasswordOrCreate']

async def run_update_user(tg_id: int, data: Dict[str, any]) -> int:
    executor = gql.add_query("updateUser", update_user())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    response = await executor.execute(variables=data)
    return response['updateUser']

