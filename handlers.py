from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ContentType

from data import SERVICES
from config import ADMIN_CHAT_ID
import keyboards as kb

router = Router()


class OrderForm(StatesGroup):
    waiting_name = State()
    waiting_phone = State()


WELCOME_TEXT = (
    "👋 <b>Webot agentligiga xush kelibsiz!</b>\n\n"
    "Biz veb-sayt va Telegram bot yaratish xizmatlarini taqdim etamiz.\n"
    "Quyidagi bo'limlardan birini tanlang:"
)

CONTACT_TEXT = (
    "📞 <b>Biz bilan bog'lanish</b>\n\n"
    "Savollaringiz bo'lsa yoki maxsus loyiha muhokama qilmoqchi bo'lsangiz, "
    "\"Buyurtma berish\" tugmasi orqali ariza qoldiring — tez orada siz bilan bog'lanamiz."
)


def tariff_text(category: str, tariff_key: str) -> str:
    tariff = SERVICES[category]["tariffs"][tariff_key]
    features = "\n".join(f"✓ {f}" for f in tariff["features"])
    popular_badge = " ⭐ <b>MASHHUR</b>" if tariff["popular"] else ""
    return (
        f"<b>{tariff['name']}</b>{popular_badge}\n"
        f"💵 <b>{tariff['price']}</b>\n"
        f"<i>{tariff['desc']}</i>\n\n"
        f"{features}"
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=kb.main_menu_kb())


@router.message(Command("narxlar"))
async def cmd_prices(message: Message):
    await message.answer("💰 <b>Narxlar bo'limini tanlang:</b>", reply_markup=kb.prices_categories_kb())


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=kb.main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "menu:prices")
async def cb_prices_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "💰 <b>Narxlar bo'limini tanlang:</b>", reply_markup=kb.prices_categories_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "menu:contact")
async def cb_contact(callback: CallbackQuery):
    await callback.message.edit_text(CONTACT_TEXT, reply_markup=kb.main_menu_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("cat:"))
async def cb_category(callback: CallbackQuery):
    category = callback.data.split(":")[1]
    title = SERVICES[category]["title"]
    await callback.message.edit_text(
        f"{title}\n\nQuyidagi tariflardan birini tanlang:",
        reply_markup=kb.tariffs_kb(category),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("tariff:"))
async def cb_tariff(callback: CallbackQuery):
    _, category, tariff_key = callback.data.split(":")
    await callback.message.edit_text(
        tariff_text(category, tariff_key),
        reply_markup=kb.tariff_detail_kb(category, tariff_key),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order:") & ~F.data.contains("cancel"))
async def cb_start_order(callback: CallbackQuery, state: FSMContext):
    _, category, tariff_key = callback.data.split(":")
    tariff = SERVICES[category]["tariffs"][tariff_key]

    await state.update_data(category=category, tariff_key=tariff_key, tariff_name=tariff["name"])
    await state.set_state(OrderForm.waiting_name)

    await callback.message.answer(
        f"Siz <b>{SERVICES[category]['title'].split()[1]} — {tariff['name']}</b> tarifini tanladingiz.\n\n"
        "✍️ Iltimos, <b>ismingizni</b> kiriting:",
        reply_markup=kb.cancel_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "order:cancel")
async def cb_cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Buyurtma bekor qilindi.", reply_markup=kb.remove_kb())
    await callback.message.answer(WELCOME_TEXT, reply_markup=kb.main_menu_kb())
    await callback.answer()


@router.message(OrderForm.waiting_name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(OrderForm.waiting_phone)
    await message.answer(
        "📱 Endi <b>telefon raqamingizni</b> yuboring (tugma orqali yoki qo'lda yozing):",
        reply_markup=kb.phone_request_kb(),
    )


@router.message(OrderForm.waiting_phone, F.content_type == ContentType.CONTACT)
async def process_phone_contact(message: Message, state: FSMContext, bot: Bot):
    await finalize_order(message, state, bot, phone=message.contact.phone_number)


@router.message(OrderForm.waiting_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext, bot: Bot):
    await finalize_order(message, state, bot, phone=message.text.strip())


async def finalize_order(message: Message, state: FSMContext, bot: Bot, phone: str):
    data = await state.get_data()
    user = message.from_user

    order_text = (
        "🆕 <b>Yangi buyurtma!</b>\n\n"
        f"👤 Ism: {data.get('name')}\n"
        f"📱 Telefon: {phone}\n"
        f"🛠 Tarif: {data.get('tariff_name')}\n"
        f"🔗 Telegram: @{user.username if user.username else 'yo\u2018q'} (ID: {user.id})"
    )

    await bot.send_message(ADMIN_CHAT_ID, order_text)

    await message.answer(
        "✅ <b>Buyurtmangiz qabul qilindi!</b>\nTez orada siz bilan bog'lanamiz. Rahmat!",
        reply_markup=kb.remove_kb(),
    )
    await message.answer(WELCOME_TEXT, reply_markup=kb.main_menu_kb())
    await state.clear()
