from aiogram.fsm.state import State, StatesGroup


class BuyProxy(StatesGroup):
    Type = State()
    Country = State()
    Quantity = State()
    SelectPeriod = State()
    ConfirmAvailability = State()
    PaymentProcess = State()


class CheckerProxy(StatesGroup):
    Choose = State()


class TopUp(StatesGroup):
    TypeTopUp = State()
    AmountTopUp = State()
