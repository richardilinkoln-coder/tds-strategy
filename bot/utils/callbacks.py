from aiogram.filters.callback_data import CallbackData


class StrategyCB(CallbackData, prefix="strat"):
    strategy_id: str


class PartyCB(CallbackData, prefix="party"):
    strategy_id: str
    party_size: str


class NavCB(CallbackData, prefix="nav"):
    action: str
    strategy_id: str = "_"
