from aiogram.filters.state import State, StatesGroup

class LanguageState(StatesGroup):
    select = State()
    
class FindTaxiState(StatesGroup):
    set_from_address = State()
    set_to_address = State()
    confirmation = State()
    
class TaxiState(StatesGroup):
    set_my_live_location = State()