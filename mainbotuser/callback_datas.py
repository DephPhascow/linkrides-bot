from aiogram.filters.callback_data import CallbackData
    
class TariffCallbackData(CallbackData, prefix="tariff"):
    pk: int
    price: float

class ApplicationCallbackData(CallbackData, prefix="application"):
    action: str
    pk: int