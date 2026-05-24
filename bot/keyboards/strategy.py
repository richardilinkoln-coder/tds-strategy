from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config.strategies import (
    PARTY_SIZE_META,
    STRATEGIES,
    get_available_party_sizes,
)
from bot.utils.callbacks import NavCB, PartyCB, StrategyCB


def _strategy_button_text(strategy_id: str) -> str:
    strategy = STRATEGIES[strategy_id]
    return f"{strategy['emoji']} {strategy['name']}"


def menu_keyboard():
    builder = InlineKeyboardBuilder()
    for strategy_id in STRATEGIES:
        builder.button(
            text=_strategy_button_text(strategy_id),
            callback_data=StrategyCB(strategy_id=strategy_id).pack(),
        )
    builder.adjust(2)
    return builder.as_markup()


def party_keyboard(strategy_id: str):
    builder = InlineKeyboardBuilder()

    available_sizes = get_available_party_sizes(strategy_id)
    for size in available_sizes:
        meta = PARTY_SIZE_META[size]
        builder.button(
            text=f"{meta['emoji']} {meta['label']}",
            callback_data=PartyCB(strategy_id=strategy_id, party_size=size).pack(),
        )

    builder.button(
        text="⬅️ Назад",
        callback_data=NavCB(action="menu", strategy_id="_").pack(),
    )
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def result_keyboard(strategy_id: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Назад",
        callback_data=NavCB(action="party", strategy_id=strategy_id).pack(),
    )
    builder.button(
        text="🏠 В меню",
        callback_data=NavCB(action="menu", strategy_id="_").pack(),
    )
    builder.adjust(2)
    return builder.as_markup()
