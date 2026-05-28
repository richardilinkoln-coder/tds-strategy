from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.callbacks import HelperCB
import random

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

    builder.button(
        text="🎧 Поддержка",
        callback_data=NavCB(action="support", strategy_id="_").pack(),
    )
    
    builder.button(
        text="🤝 Найти хелпера",
        callback_data=HelperCB(action="list").pack(),
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
    
    size_count = len(available_sizes)
    if size_count % 2 == 0:
        adjust_args = [2] * (size_count // 2) + [1]
    else:
        adjust_args = [2] * (size_count // 2) + [1, 1]
    
    builder.adjust(*adjust_args)
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
    builder.adjust(1, 1)
    return builder.as_markup()


def support_keyboard(support_agents: list[str]):
    builder = InlineKeyboardBuilder()
    
    if support_agents:
        builder.button(
            text="🎲 Случайный агент",
            url=f"https://t.me/{random.choice(support_agents)}"
        )
    
    builder.button(
        text="⬅️ Назад",
        callback_data=NavCB(action="menu", strategy_id="_").pack()
    )
    
    builder.adjust(1)
    return builder.as_markup()
