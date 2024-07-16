from aiogram.filters.callback_data import CallbackData
    
class TestCallbackData(CallbackData, prefix="test"):
    test: str