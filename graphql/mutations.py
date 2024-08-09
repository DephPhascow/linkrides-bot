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
            "phoneNumber": "String",
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
def find_taxi():
    return gen_mutate(
        name="findTaxi",
        request="__typename",
        var={
            "tariffId": "Int!",
            "fromLatitude": "Float!",
            "fromLongitude": "Float!",
            "toLatitude": "Float",
            "toLongitude": "Float",
        }
    )
def taxi_cancel_application():
    return gen_mutate(
        name="taxiCancelApplication",
        var={
            "applicationId": "Int!",
        }
    )

def taxi_accept_application():
    return gen_mutate(
        name="taxiAcceptApplication",
        var={
            "applicationId": "Int!",
        }
    )
    
async def run_taxi_accept_application(tg_id: int, application_id: int) -> bool:
    executor = gql.add_query("taxi_accept_application", taxi_accept_application())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    response = await executor.execute(variables={
        "applicationId": application_id
    })
    return response['taxiAcceptApplication']

async def run_taxi_cancel_application(tg_id: int, application_id: int) -> bool:
    executor = gql.add_query("taxi_cancel_application", taxi_cancel_application())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    response = await executor.execute(variables={
        "applicationId": application_id
    })
    return response['taxiCancelApplication']

async def run_find_taxi(tg_id: int, tariff_id: int, from_latitude: float, from_longitude: float, to_latitude: Optional[float] = None, to_longitude: Optional[float] = None) -> int:
    executor = gql.add_query("findTaxi", find_taxi())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    kwargs = {
        "tariffId": tariff_id,
        "fromLatitude": from_latitude,
        "fromLongitude": from_longitude,
    }
    if to_latitude:
        kwargs['toLatitude'] = to_latitude
    if to_longitude:
        kwargs['toLongitude'] = to_longitude
    response = await executor.execute(variables=kwargs)
    return response['findTaxi']

async def run_taxi_set_status(tg_id: int, status: DrivingStatus) -> int:
    executor = gql.add_query("taxi_set_status", taxi_set_status())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    response = await executor.execute(variables={
        "status": status.value
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
        "status": status.value
    })
    return response['taxiSetMyCurrentLocation']

async def run_get_password_or_create(tg_id: int, first_name: str, last_name: Optional[str] = None, username: Optional[str] = None, phone_number: str = None) -> str:
    executor = gql.add_query("getPasswordOrCreate", get_password())
    response = await executor.execute(variables={
        "tgId": f'{tg_id}',
        "firstName": first_name,
        "lastName": last_name,
        "username": username,
        "phoneNumber": phone_number,
    }, ignore_middlewares=['auth'])
    return response['getPasswordOrCreate']

async def run_update_user(tg_id: int, data: Dict[str, any]) -> int:
    executor = gql.add_query("updateUser", update_user())
    user: UserModel = await UserModel.get_or_none(uid=tg_id)
    auth: AuthMiddleware = executor['middleware__auth']
    await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
    response = await executor.execute(variables=data)
    return response['updateUser']

