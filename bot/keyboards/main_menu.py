from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.config.strategies import STRATEGIES 
from bot.utils.callbacks import HelperCB  # <-- Добавили импорт фабрики

def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    
    for strat_key, strat_data in STRATEGIES.items():
        builder.button(
            text=strat_data["name"], 
            callback_data=f"strat_{strat_key}"
        )
    
    # Теперь кнопка отправляет правильный сигнал, который понимает helpers.py
    builder.button(
        text="👥 Топ Хелперов",
        callback_data=HelperCB(action="list").pack()
    )
    
    builder.adjust(1)
    return builder.as_markup()
