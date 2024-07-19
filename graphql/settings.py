from graphql.fragments import fragment_operation_info
from models import UserModel
from .core.graphql import GraphQL, GraphQLConfig
from .core.logger import FileLogger
from .core.middlewares.auth_middleware import AuthMiddleware, Token
from constants import GRAPHQL_URL, DEBUG
import asyncio

gql = GraphQL(
    gql_config=GraphQLConfig(
        http=GRAPHQL_URL,
        DEBUG=DEBUG,
        disable_ssl=True,
    )
)

gql.add_fragment(fragment_operation_info())

async def on_save_token(token: Token, login: str):
    user = await UserModel.get_or_none(uid=login)
    user.jwt_token = token.token
    user.jwt_token_exp = token.token_exp
    user.jwt_refresh_token = token.refresh_token
    user.jwt_refresh_token_exp = token.refresh_token_exp
    await user.save()

gql.add_middleware(AuthMiddleware(gql=gql, name="auth", on_save=on_save_token))
gql.set_logger(FileLogger(file_name="gql-log.txt"))

asyncio.run(gql.init())