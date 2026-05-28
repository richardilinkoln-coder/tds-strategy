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
from aiogram.filters import Command
from aiogram.types import Message

@router.message(Command("add_helper"), IsAdmin())
async def cmd_add_helper(message: Message):
    args = message.text.split()
    
    # Проверяем, что аргументов ровно 4 (команда + 3 параметра)
    if len(args) != 4:
        # Убрали < >, добавили <code> для удобного копирования
        await message.answer(
            "❌ <b>Ошибка формата!</b>\n"
            "Используйте: <code>/add_helper ID ТГ_ник Roblox_ник</code>\n"
            "<i>Пример: /add_helper 123456789 Иван ivan_pro</i>"
        )
        return

    # Защита от ввода букв или @username вместо ID
    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("❌ <b>Ошибка:</b> ID должен быть числом! Бот не умеет добавлять по @username.")
        return

    tg_nick = args[2]
    roblox_nick = args[3]

    success = await db.add_helper(user_id, tg_nick, roblox_nick)
    if success:
        await message.answer(f"✅ Хелпер {tg_nick} (Roblox: {roblox_nick}) успешно добавлен в базу.")
    else:
        await message.answer("⚠️ Этот пользователь уже числится в списке хелперов.")

@router.message(Command("del_helper"), IsAdmin())
async def cmd_del_helper(message: Message):
    args = message.text.split()
    
    if len(args) != 2:
        await message.answer("❌ <b>Ошибка формата!</b>\nИспользуйте: <code>/del_helper ID</code>")
        return
        
    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("❌ <b>Ошибка:</b> ID должен быть числом!")
        return

    success = await db.delete_helper(user_id)
    if success:
        await message.answer(f"✅ Пользователь с ID <code>{user_id}</code> удален из списка хелперов. Его отзывы сохранены.")
    else:
        await message.answer("⚠️ Хелпер с таким ID не найден в базе.")

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
    # Просто вызываем нашу новую универсальную функцию!
    await send_helper_card(callback, callback_data.helper_id)
    
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
# ================= СИСТЕМА ОТЗЫВОВ (FSM) =================
# ================= СИСТЕМА ОТЗЫВОВ (FSM) =================
# ================= СИСТЕМА ОТЗЫВОВ (FSM) =================

@router.callback_query(ReviewCB.filter(F.action == "start"))
async def start_review(callback: CallbackQuery, callback_data: ReviewCB, state: FSMContext):
    await state.set_state(ReviewStates.waiting_for_review_text)
    await state.update_data(helper_id=callback_data.helper_id, comment=None)
    
    # ПРОВЕРКА: Оставлял ли юзер отзыв ранее?
    existing_review = await db.get_user_review(callback_data.helper_id, callback.from_user.id)
    
    if existing_review:
        old_stars, old_comment = existing_review
        text = (
            f"⚠️ <b>Внимание!</b> Вы уже оставляли отзыв (⭐ {old_stars}).\n\n"
            "Если вы введете новый текст и выберете оценку, <b>старый отзыв будет перезаписан</b>.\n"
            "Введите новый текст в чат (или нажмите на оценку, чтобы оставить отзыв без текста):"
        )
    else:
        text = (
            "✍️ <b>Оставление отзыва</b>\n\n"
            "Введите текст отзыва в чат, а затем нажмите на оценку ниже.\n"
            "Если хотите оставить отзыв без текста — просто нажмите на оценку."
        )

    await callback.answer()
    await _safe_edit(callback.message, text, reply_markup=review_stars_keyboard(callback_data.helper_id))
    
    prompt_msg = await callback.message.answer("Введите комментарий к отзыву:")
    await state.update_data(prompt_msg_id=prompt_msg.message_id)

@router.message(ReviewStates.waiting_for_review_text)
async def catch_review_text(message: Message, state: FSMContext):
    data = await state.get_data()
    user_msg_ids = data.get("user_msg_ids", [])
    user_msg_ids.append(message.message_id)
    
    success_msg = await message.answer("✅ <b>Текст сохранен!</b> Теперь нажмите на кнопку с количеством звезд выше, чтобы отправить отзыв.")
    
    await state.update_data(
        comment=message.text, 
        user_msg_ids=user_msg_ids,
        success_msg_id=success_msg.message_id
    )

@router.callback_query(ReviewCB.filter(F.action == "save"), ReviewStates.waiting_for_review_text)
async def save_review_callback(callback: CallbackQuery, callback_data: ReviewCB, state: FSMContext):
    data = await state.get_data()
    comment = data.get("comment")
    
    # Очистка чата от временных сообщений
    chat_id = callback.message.chat.id
    msg_ids_to_delete = []
    
    if "prompt_msg_id" in data: msg_ids_to_delete.append(data["prompt_msg_id"])
    if "success_msg_id" in data: msg_ids_to_delete.append(data["success_msg_id"])
    if "user_msg_ids" in data: msg_ids_to_delete.extend(data["user_msg_ids"])
        
    for msg_id in msg_ids_to_delete:
        try:
            await callback.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass
            
    # Захватываем юзернейм автора (если его нет - берем Имя)
    reviewer_username = callback.from_user.username or callback.from_user.first_name
    
    # Сохраняем в БД с юзернеймом
    await db.save_review(
        helper_id=callback_data.helper_id,
        user_id=callback.from_user.id,
        stars=callback_data.stars,
        comment=comment,
        reviewer_username=reviewer_username
    )
    
    await state.clear()
    await callback.answer("✅ Отзыв успешно сохранен!", show_alert=True)
    
    # Возвращаемся в карточку
    await send_helper_card(callback, callback_data.helper_id)

# НОВОЕ: Обработчик кнопки "Все отзывы"
@router.callback_query(ReviewCB.filter(F.action == "all"))
async def show_all_reviews(callback: CallbackQuery, callback_data: ReviewCB):
    reviews = await db.get_all_reviews(callback_data.helper_id)
    
    if not reviews:
        await callback.answer("Отзывов пока нет.", show_alert=True)
        return
        
    text = "📋 <b>Все отзывы:</b>\n\n"
    for r_id, r_stars, r_comment, r_username in reviews:
        stars_str = "⭐" * r_stars
        user_str = f"@{r_username}" if r_username else "Аноним"
        comment_str = f" - <i>«{r_comment}»</i>" if r_comment else ""
        text += f"[ID: {r_id}] {stars_str} от {user_str}{comment_str}\n\n"
        
    # Кнопка возврата к карточке
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад к хелперу", callback_data=HelperCB(action="card", helper_id=callback_data.helper_id).pack())
    
    await callback.answer()
    await _safe_edit(callback.message, text, reply_markup=builder.as_markup())

# НОВОЕ: Команда удаления отзыва для админов (Путь А)
@router.message(Command("del_review"), IsAdmin())
async def cmd_del_review(message: Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ Формат: <code>/del_review ID_отзыва</code>\nID отзыва указан в скобках [ID: ...] в карточке.")
        return
        
    try:
        review_id = int(args[1])
    except ValueError:
        await message.answer("❌ ID должен быть числом.")
        return

    success = await db.delete_review(review_id)
    if success:
        await message.answer(f"✅ Отзыв [ID: {review_id}] успешно удален из базы.")
    else:
        await message.answer("⚠️ Отзыв с таким ID не найден.")

# Вспомогательная функция для рендеринга карточки (чтобы не дублировать код)
async def send_helper_card(callback: CallbackQuery, helper_id: int):
    helper = await db.get_helper_info(helper_id)
    _, tg_nick, roblox_nick, avg_rating, review_count = helper
    
    text = (
        f"👤 <b>Хелпер:</b> {tg_nick}\n"
        f"🎮 <b>Roblox ник:</b> <code>{roblox_nick}</code>\n"
        f"⭐ <b>Рейтинг:</b> {avg_rating:.1f} (отзывов: {review_count})\n\n"
    )
    
    # Показываем 3 последних отзыва с их ID
    reviews = await db.get_latest_reviews(helper_id, limit=3)
    if reviews:
        text += "💬 <b>Последние отзывы:</b>\n"
        for r_id, r_stars, r_comment, r_username in reviews:
            stars_str = "⭐" * r_stars
            user_str = f"@{r_username}" if r_username else "Аноним"
            comment_str = f" - <i>«{r_comment}»</i>" if r_comment else ""
            text += f"[ID: {r_id}] {stars_str} от {user_str}{comment_str}\n"
            
    await _safe_edit(callback.message, text, reply_markup=helper_card_keyboard(helper_id, tg_nick))
# meowц
