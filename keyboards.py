from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from data import SERVICES


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 Narxlar", callback_data="menu:prices")
    builder.button(text="📞 Aloqa", callback_data="menu:contact")
    builder.adjust(1)
    return builder.as_markup()


def prices_categories_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Veb-sayt narxlari", callback_data="cat:web")
    builder.button(text="🤖 Bot narxlari", callback_data="cat:bot")
    builder.button(text="⬅️ Orqaga", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def tariffs_kb(category: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, tariff in SERVICES[category]["tariffs"].items():
        label = tariff["name"]
        if tariff["popular"]:
            label += " ⭐"
        builder.button(text=label, callback_data=f"tariff:{category}:{key}")
    builder.button(text="⬅️ Orqaga", callback_data="menu:prices")
    builder.adjust(1)
    return builder.as_markup()


def tariff_detail_kb(category: str, tariff_key: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Buyurtma berish", callback_data=f"order:{category}:{tariff_key}")
    builder.button(text="⬅️ Orqaga", callback_data=f"cat:{category}")
    builder.adjust(1)
    return builder.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Bekor qilish", callback_data="order:cancel")
    builder.adjust(1)
    return builder.as_markup()


def phone_request_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="📱 Raqamni yuborish", request_contact=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def remove_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
