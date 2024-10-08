from typing import Optional, Dict, Any
from aiogram.types import TelegramObject, User
from aiogram.utils.i18n import I18nMiddleware, I18n
from models import UserModel


class LanguageMiddleware(I18nMiddleware):
    def __init__(
            self,
            i18n: I18n,
            i18n_key: Optional[str] = "i18n",
            middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user: Optional[User] = data.get("event_from_user", None)
        user = await UserModel.filter(uid=event_from_user.id).first()
        if not user:
            return event_from_user.language_code
        return user.language
