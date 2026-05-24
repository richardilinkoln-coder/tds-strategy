import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from bot.config.strategies import PARTY_SIZE_META, get_available_party_sizes, get_strategy
from bot.keyboards.strategy import menu_keyboard, party_keyboard, result_keyboard
from bot.utils.callbacks import NavCB, PartyCB, StrategyCB

router = Router()
logger = logging.getLogger(__name__)


def _is_strategy_trigger(text: str | None) -> bool:
    return bool(text and text.strip().lower() == "стратегия")


def _build_menu_text() -> str:
    return (
        "🎮 <b>Выбери режим:</b>\n\n"
        "Нажми на нужную карту, чтобы увидеть доступные размеры команды."
    )


def _build_party_text(strategy_id: str) -> str:
    strategy = get_strategy(strategy_id)
    if not strategy:
        return "❌ <b>Неизвестный режим</b>\n\nЭтот режим больше недоступен."

    name = str(strategy["name"])
    emoji = str(strategy["emoji"])
    return (
        f"🎮 <b>Режим:</b> {name} {emoji}\n\n"
        "Выбери размер команды:"
    )


def _build_result_text(strategy_id: str, party_size: str, link: str) -> str:
    strategy = get_strategy(strategy_id)
    if not strategy:
        return "❌ <b>Ошибка</b>\n\nНе удалось найти режим."

    strategy_name = str(strategy["name"])
    strategy_emoji = str(strategy["emoji"])
    size_meta = PARTY_SIZE_META.get(party_size)
    size_label = size_meta["label"] if size_meta else party_size
    size_emoji = size_meta["emoji"] if size_meta else "👥"

    return (
        "✅ <b>Strategy found!</b>\n\n"
        f"{strategy_emoji} <b>{strategy_name}</b>\n"
        f"{size_emoji} <b>{size_label}</b>\n\n"
        f"📄 <b>Документ:</b>\n"
        f'<a href="{link}">Открыть документ</a>'
    )


async def _safe_edit(message: Message | None, text: str, reply_markup=None) -> None:
    if message is None:
        return

    try:
        await message.edit_text(text, reply_markup=reply_markup, parse_mode='HTML', disable_web_page_preview=True)
    except TelegramBadRequest as exc:
        if "message is not modified" in str(exc).lower():
            return
        raise


@router.message(F.text.func(_is_strategy_trigger))
async def on_strategy_trigger(message: Message) -> None:
    logger.info(
        "Strategy menu requested by user_id=%s chat_id=%s",
        message.from_user.id if message.from_user else None,
        message.chat.id,
    )
    await message.answer(_build_menu_text(), reply_markup=menu_keyboard(), parse_mode='HTML', disable_web_page_preview=True)


@router.callback_query(StrategyCB.filter())
async def on_strategy_selected(callback: CallbackQuery, callback_data: StrategyCB) -> None:
    strategy = get_strategy(callback_data.strategy_id)
    if not strategy:
        logger.warning("Unknown strategy_id=%s", callback_data.strategy_id)
        await callback.answer("Этот режим больше недоступен", show_alert=True)
        await _safe_edit(
            callback.message,
            "❌ <b>Неизвестный режим</b>\n\nЭтот режим больше недоступен.",
            reply_markup=menu_keyboard(),
        )
        return

    logger.info(
        "Strategy selected strategy_id=%s user_id=%s chat_id=%s",
        callback_data.strategy_id,
        callback.from_user.id if callback.from_user else None,
        callback.message.chat.id if callback.message else None,
    )
    await callback.answer()
    await _safe_edit(
        callback.message,
        _build_party_text(callback_data.strategy_id),
        reply_markup=party_keyboard(callback_data.strategy_id),
    )


@router.callback_query(PartyCB.filter())
async def on_party_selected(callback: CallbackQuery, callback_data: PartyCB) -> None:
    strategy = get_strategy(callback_data.strategy_id)
    if not strategy:
        logger.warning("Unknown strategy on party callback strategy_id=%s", callback_data.strategy_id)
        await callback.answer("Не удалось найти режим", show_alert=True)
        await _safe_edit(
            callback.message,
            "❌ <b>Ошибка</b>\n\nНе удалось найти режим.",
            reply_markup=menu_keyboard(),
        )
        return

    available_sizes = get_available_party_sizes(callback_data.strategy_id)
    if callback_data.party_size not in available_sizes:
        logger.warning(
            "Unavailable party size strategy_id=%s party_size=%s",
            callback_data.strategy_id,
            callback_data.party_size,
        )
        await callback.answer("Этот размер команды недоступен", show_alert=True)
        await _safe_edit(
            callback.message,
            "⚠️ <b>Этот размер команды недоступен</b>\n\n"
            "Выбери другой вариант или вернись назад.",
            reply_markup=party_keyboard(callback_data.strategy_id),
        )
        return

    modes = strategy.get("modes", {})
    if not isinstance(modes, dict):
        logger.error("Invalid modes config for strategy_id=%s", callback_data.strategy_id)
        await callback.answer("Ошибка конфигурации", show_alert=True)
        await _safe_edit(
            callback.message,
            "❌ <b>Ошибка конфигурации</b>\n\n"
            "У этого режима некорректно настроены ссылки.",
            reply_markup=menu_keyboard(),
        )
        return

    link = modes.get(callback_data.party_size)
    if not link:
        logger.warning(
            "Missing link strategy_id=%s party_size=%s",
            callback_data.strategy_id,
            callback_data.party_size,
        )
        await callback.answer("Ссылка для этого размера отсутствует", show_alert=True)
        await _safe_edit(
            callback.message,
            "⚠️ <b>Ссылка для этого размера отсутствует</b>\n\n"
            "Проверь конфиг и добавь нужный URL.",
            reply_markup=party_keyboard(callback_data.strategy_id),
        )
        return

    logger.info(
        "Strategy result strategy_id=%s party_size=%s user_id=%s chat_id=%s",
        callback_data.strategy_id,
        callback_data.party_size,
        callback.from_user.id if callback.from_user else None,
        callback.message.chat.id if callback.message else None,
    )
    await callback.answer()
    await _safe_edit(
        callback.message,
        _build_result_text(callback_data.strategy_id, callback_data.party_size, link),
        reply_markup=result_keyboard(callback_data.strategy_id),
    )


@router.callback_query(NavCB.filter())
async def on_navigation(callback: CallbackQuery, callback_data: NavCB) -> None:
    await callback.answer()

    if callback_data.action == "menu":
        logger.info(
            "Navigation to menu user_id=%s chat_id=%s",
            callback.from_user.id if callback.from_user else None,
            callback.message.chat.id if callback.message else None,
        )
        await _safe_edit(
            callback.message,
            _build_menu_text(),
            reply_markup=menu_keyboard(),
        )
        return

    if callback_data.action == "party":
        if not get_strategy(callback_data.strategy_id):
            logger.warning("Navigation requested for unknown strategy_id=%s", callback_data.strategy_id)
            await _safe_edit(
                callback.message,
                "❌ <b>Неизвестный режим</b>\n\nВернись в меню и выбери другой вариант.",
                reply_markup=menu_keyboard(),
            )
            return

        logger.info(
            "Navigation back to party strategy_id=%s user_id=%s chat_id=%s",
            callback_data.strategy_id,
            callback.from_user.id if callback.from_user else None,
            callback.message.chat.id if callback.message else None,
        )
        await _safe_edit(
            callback.message,
            _build_party_text(callback_data.strategy_id),
            reply_markup=party_keyboard(callback_data.strategy_id),
        )
        return

    logger.warning("Unknown navigation action=%s", callback_data.action)
    await _safe_edit(
        callback.message,
        "❌ <b>Ошибка навигации</b>\n\nНеизвестное действие.",
        reply_markup=menu_keyboard(),
    )
