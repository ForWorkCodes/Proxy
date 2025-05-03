from aiogram.fsm.state import State, StatesGroup

class BuyProxy(StatesGroup):
    Type = State()
    Country = State()
    Quantity = State()
    ConfirmAvailability = State()
    PaymentChoice = State()
    PaymentProcess = State()
    ProxyDelivery = State()
