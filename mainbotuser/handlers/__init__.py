from .main import main_bot_router
from .driving import main_bot_router
from .select_lang import main_bot_router
from .find_taxi import main_bot_router
from .statistic import main_bot_router
from .profile import main_bot_router
from .faq import main_bot_router


from .unknown import main_bot_router

__all__ = [
    "main_bot_router",
]
