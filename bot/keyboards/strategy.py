from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.callbacks import HelperCB
import random
from bot.config.settings import SUPPORT_AGENTS

from bot.config.strategies import (
    PARTY_SIZE_META,
    STRATEGIES,
    get_available_party_sizes,
)
from bot.utils.callbacks import NavCB, PartyCB, StrategyCB


def _strategy_button_text(strategy_id: str) -> str:
    strategy = STRATEGIES[strategy_id]
    return f"{strategy['emoji']} {strategy['name']}"


# Не забудь добавить импорт нового коллбека в начале файла:
# from bot.utils.callbacks import HelperCB

def menu_keyboard():
    builder = InlineKeyboardBuilder()
    for strategy_id in STRATEGIES:
        builder.button(
            text=_strategy_button_text(strategy_id),
            callback_data=StrategyCB(strategy_id=strategy_id).pack(),
        )

    # --- КНОПКА ПОДДЕРЖКИ (Предпоследняя) ---
    builder.button(
        text="🎧 Поддержка",
        callback_data=NavCB(action="support", strategy_id="_").pack(),
    )
    
    # --- НОВАЯ КНОПКА ---
    builder.button(
        text="🤝 Найти хелпера",
        callback_data=HelperCB(action="list").pack(),
    )
    # --------------------
    
    builder.adjust(2) # aiogram сам перенесет кнопку хелперов на новую строку, если количество стратегий четное
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
    
    # Динамическая раскладка: размеры по 2 в ряду, Назад отдельно
    size_count = len(available_sizes)
    if size_count % 2 == 0:
        # Четное количество размеров: (2, 2, ..., 1)
        adjust_args = [2] * (size_count // 2) + [1]
    else:
        # Нечетное количество размеров: (2, 2, ..., 1, 1)
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


def support_keyboard():
    builder = InlineKeyboardBuilder()
    
    # Создаем список кнопок
    # Вместо готовой строки мы передаем выбор рандома прямо в генерацию кнопки!
    builder.button(
        text="🎲 Случайный агент",
        url=f"https://t.me/{random.choice(SUPPORT_AGENTS).replace('@', '')}"
    )
    
    builder.button(
        text="⬅️ Назад",
        callback_data=NavCB(action="menu", strategy_id="_").pack()
    )
    
    builder.adjust(1)
    return builder.as_markup()
