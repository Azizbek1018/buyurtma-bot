import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "7450764374"))

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi! .env faylida yoki Render Environment Variables bo'limida "
        "BOT_TOKEN o'zgaruvchisini kiriting."
    )
