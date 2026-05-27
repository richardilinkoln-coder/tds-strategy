from aiogram.filters.callback_data import CallbackData


class StrategyCB(CallbackData, prefix="strat"):
    strategy_id: str


class PartyCB(CallbackData, prefix="party"):
    strategy_id: str
    party_size: str


class NavCB(CallbackData, prefix="nav"):
    action: str
    strategy_id: str = "_"


from aiogram.filters.callback_data import CallbackData

# ... твои текущие классы ...

class HelperCB(CallbackData, prefix="hlp"):
    action: str  # 'list', 'card'
    helper_id: int = 0

class ReviewCB(CallbackData, prefix="rev"):
    action: str  # 'start', 'save', 'all'
    helper_id: int
    stars: int = 0
