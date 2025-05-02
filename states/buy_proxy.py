from aiogram.fsm.state import State, StatesGroup

class BuyProxyStates(StatesGroup):
    ChoosingType = State()
    ChoosingCountry = State()
    ChoosingDuration = State()
    ChoosingQuantity = State()
    Confirming = State()
