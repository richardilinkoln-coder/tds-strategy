# bot/handlers/helpers.py
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from bot.database import db
from bot.utils.callbacks import HelperCB, ReviewCB
from bot.keyboards.helpers import helpers_list_keyboard, helper_card_keyboard, review_stars_keyboard
from bot.states.helpers import ReviewStates
from bot.filters.admin import IsAdmin

router = Router()
logger = logging.getLogger(__name__)

async def _safe_edit(message: Message | None, text: str, reply_markup=None) -> None:
    if message is None:
        return
    try:
        await message.edit_text(text, reply_markup=reply_markup, parse_mode='HTML', disable_web_page_preview=True)
    except TelegramBadRequest as exc:
        if "message is not modified" in str(exc).lower():
            return
        raise

# ================= АДМИНКА =================
@router.message(Command("add_helper"), IsAdmin())
async def cmd_add_helper(message: Message):
    # Ожидаемый формат: /add_helper 123456789 @tg_nick RobloxNick
    args = message.text.split()[1:]
    if len(args) != 3:
        await message.answer("❌ Формат: /add_helper <tg_id> <tg_nick> <roblox_nick>")
        return
    
    try:
        user_id = int(args[0])
        tg_nick = args[1]
        roblox_nick = args[2]
    except ValueError:
        await message.answer("❌ ID пользователя должно быть числом.")
        return

    success = await db.add_helper(user_id, tg_nick, roblox_nick)
    if success:
        await message.answer(f"✅ Хелпер {tg_nick} (Roblox: {roblox_nick}) успешно добавлен в базу.")
    else:
        await message.answer("⚠️ Этот пользователь уже добавлен как хелпер.")

@router.message(Command("del_helper"), IsAdmin())
async def cmd_del_helper(message: Message):
    # Ожидаемый формат: /del_helper <tg_id>
    args = message.text.split()[1:]
    if len(args) != 1:
        await message.answer("❌ Формат: /del_helper <tg_id>")
        return
    
    try:
        user_id = int(args[0])
    except ValueError:
        await message.answer("❌ ID пользователя должно быть числом.")
        return

    success = await db.delete_helper(user_id)
    if success:
        await message.answer(f"✅ Пользователь с ID <code>{user_id}</code> успешно удален из списка хелперов (все отзывы также стерты).")
    else:
        await message.answer("⚠️ Пользователь с таким ID не найден в списке хелперов.")

# ================= МЕНЮ ХЕЛПЕРОВ =================
@router.callback_query(HelperCB.filter(F.action == "list"))
async def show_helpers_list(callback: CallbackQuery, state: FSMContext):
    await state.clear() # На всякий случай сбрасываем стейты
    helpers_data = await db.get_helpers_top()
    
    text = "🤝 <b>Раздел хелперов</b>\n\nЗдесь вы можете найти опытных игроков. Выберите хелпера из списка:"
    if not helpers_data:
        text = "🤝 <b>Раздел хелперов</b>\n\nПока что список пуст."
        
    await callback.answer()
    await _safe_edit(callback.message, text, reply_markup=helpers_list_keyboard(helpers_data))

@router.callback_query(HelperCB.filter(F.action == "card"))
async def show_helper_card(callback: CallbackQuery, callback_data: HelperCB, state: FSMContext):
    await state.clear()
    helper = await db.get_helper_info(callback_data.helper_id)
    if not helper:
        await callback.answer("Хелпер не найден", show_alert=True)
        return
    
    _, tg_nick, roblox_nick, avg_rating, review_count = helper
    
    text = (
        f"👤 <b>Хелпер:</b> {tg_nick}\n"
        f"🎮 <b>Roblox ник:</b> <code>{roblox_nick}</code>\n"
        f"⭐ <b>Рейтинг:</b> {avg_rating:.1f} (отзывов: {review_count})\n\n"
    )
    
    reviews = await db.get_latest_reviews(callback_data.helper_id, limit=3)
    if reviews:
        text += "💬 <b>Последние отзывы:</b>\n"
        for r_stars, r_comment in reviews:
            stars_str = "⭐" * r_stars
            comment_str = f" - <i>«{r_comment}»</i>" if r_comment else ""
            text += f"{stars_str}{comment_str}\n"
    else:
        text += "<i>Отзывов пока нет. Станьте первым!</i>"
        
    await callback.answer()
    await _safe_edit(callback.message, text, reply_markup=helper_card_keyboard(callback_data.helper_id, tg_nick))

# ================= СИСТЕМА ОТЗЫВОВ (FSM) =================
@router.callback_query(ReviewCB.filter(F.action == "start"))
async def start_review(callback: CallbackQuery, callback_data: ReviewCB, state: FSMContext):
    # Включаем ожидание текста, сохраняем ID хелпера
    await state.set_state(ReviewStates.waiting_for_review_text)
    await state.update_data(helper_id=callback_data.helper_id, comment=None)
    
    text = (
        "✍️ <b>Оставление отзыва</b>\n\n"
        "Если хотите оставить текстовый комментарий — <b>просто напишите его сейчас в чат</b>.\n\n"
        "Или сразу выберите оценку ниже, чтобы оставить отзыв без текста:"
    )
    await callback.answer()
    await _safe_edit(callback.message, text, reply_markup=review_stars_keyboard(callback_data.helper_id))

@router.message(ReviewStates.waiting_for_review_text)
async def catch_review_text(message: Message, state: FSMContext):
    # Ловим текст, обновляем дату в FSM и удаляем сообщение юзера, чтобы не засорять чат (если у бота есть права)
    await state.update_data(comment=message.text)
    
    try:
        await message.delete()
    except:
        pass
    
    # Отправляем подтверждение, клавиатура остается старой (мы ее не генерируем заново, просто просим нажать кнопку)
    msg = await message.answer("✅ <b>Текст сохранен!</b> Теперь нажмите на кнопку с количеством звезд, чтобы отправить отзыв.")
    
    # Автоудаление этого уведомления через 3 секунды (не блокируя бота)
    import asyncio
    asyncio.create_task(delete_message_delay(msg, 3))

async def delete_message_delay(message: Message, delay: int):
    import asyncio
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

@router.callback_query(ReviewCB.filter(F.action == "save"), ReviewStates.waiting_for_review_text)
async def save_review_callback(callback: CallbackQuery, callback_data: ReviewCB, state: FSMContext):
    # Достаем текст из памяти (если юзер ничего не писал, там будет None)
    data = await state.get_data()
    comment = data.get("comment")
    
    # Сохраняем в БД
    await db.save_review(
        helper_id=callback_data.helper_id,
        user_id=callback.from_user.id,
        stars=callback_data.stars,
        comment=comment
    )
    
    await state.clear()
    await callback.answer("✅ Отзыв успешно сохранен!", show_alert=True)
    
    # Возвращаем на карточку хелпера
    helper = await db.get_helper_info(callback_data.helper_id)
    _, tg_nick, roblox_nick, avg_rating, review_count = helper
    
    text = (
        f"👤 <b>Хелпер:</b> {tg_nick}\n"
        f"🎮 <b>Roblox ник:</b> <code>{roblox_nick}</code>\n"
        f"⭐ <b>Рейтинг:</b> {avg_rating:.1f} (отзывов: {review_count})\n\n"
    )
    
    reviews = await db.get_latest_reviews(callback_data.helper_id, limit=3)
    if reviews:
        text += "💬 <b>Последние отзывы:</b>\n"
        for r_stars, r_comment in reviews:
            stars_str = "⭐" * r_stars
            comment_str = f" - <i>«{r_comment}»</i>" if r_comment else ""
            text += f"{stars_str}{comment_str}\n"
            
    await _safe_edit(callback.message, text, reply_markup=helper_card_keyboard(callback_data.helper_id, tg_nick))
