from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.callbacks import HelperCB, ReviewCB, NavCB

def helpers_list_keyboard(helpers_data):
    builder = InlineKeyboardBuilder()
    
    # helpers_data - это список кортежей из БД: (id, tg_nick, roblox_nick, avg_rating, review_count)
    for h in helpers_data:
        helper_id, tg_nick, _, avg_rating, review_count = h
        rating_text = f"⭐ {avg_rating:.1f}" if review_count > 0 else "Нет отзывов"
        
        builder.button(
            text=f"👤 {tg_nick} ({rating_text})",
            callback_data=HelperCB(action="card", helper_id=helper_id).pack()
        )
        
    builder.button(
        text="⬅️ Назад",
        callback_data=NavCB(action="menu", strategy_id="_").pack()
    )
    
    builder.adjust(1)
    return builder.as_markup()

def helper_card_keyboard(helper_id: int, tg_nick: str):
    builder = InlineKeyboardBuilder()
    
    # Кнопка Оставить отзыв
    builder.button(
        text="✍️ Оставить отзыв",
        callback_data=ReviewCB(action="start", helper_id=helper_id, stars=0).pack()
    )
    # НОВАЯ КНОПКА: Все отзывы (action="all")
    builder.button(
        text="📋 Все отзывы",
        callback_data=ReviewCB(action="all", helper_id=helper_id, stars=0).pack()
    )
    # Кнопка Назад
    builder.button(
        text="🔙 Назад к списку",
        callback_data=HelperCB(action="list").pack()  # <--- Заменили "helpers_top" на правильный коллбек
    )
    
    builder.adjust(1, 1, 1) # Каждая кнопка на новой строке
    return builder.as_markup()

def review_stars_keyboard(helper_id: int):
    builder = InlineKeyboardBuilder()
    
    # Кнопки от 1 до 5 звезд
    for i in range(1, 6):
        builder.button(
            text=f"⭐ {i}",
            callback_data=ReviewCB(action="save", helper_id=helper_id, stars=i).pack()
        )
        
    builder.button(
        text="❌ Отмена",
        callback_data=HelperCB(action="card", helper_id=helper_id).pack()
    )
    
    # Звезды в один ряд (5), кнопка отмены снизу (1)
    builder.adjust(5, 1)
    return builder.as_markup()
