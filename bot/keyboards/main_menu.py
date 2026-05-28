from aiogram.utils.keyboard import InlineKeyboardBuilder
# Если твои стратегии лежат в bot.config.strategies, импортируй их
from bot.config.strategies import STRATEGIES 

def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    
    # Сначала генерируем кнопки для всех стратегий из твоего словаря
    for strat_key, strat_data in STRATEGIES.items():
        builder.button(
            text=strat_data["name"], 
            callback_data=f"strat_{strat_key}"
        )
    
    # Затем жестко добавляем кнопку Хелперов в самый низ (или перенеси выше)
    builder.button(
        text="👥 Топ Хелперов",
        callback_data="helpers_top"
    )
    
    builder.adjust(1) # По 1 кнопке в ряд
    return builder.as_markup()
