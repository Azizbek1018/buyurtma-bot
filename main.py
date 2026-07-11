import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import router

logging.basicConfig(level=logging.INFO)


async def handle_health(request: web.Request) -> web.Response:
    # UptimeRobot shu manzilga har 5 daqiqada so'rov yuboradi,
    # shunda Render bepul Web Service'ni "uxlab qolishdan" saqlaydi
    return web.Response(text="Bot ishlayapti ✅")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_health)
    app.router.add_get("/healthz", handle_health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Health-check server {port}-portda ishga tushdi")


async def start_bot():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # Eski (webhook orqali kelgan) yangilanishlarni tozalab, polling boshlaymiz
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Bot polling rejimida ishga tushdi...")
    await dp.start_polling(bot)


async def main():
    # Health-check server va bot polling bir vaqtda, parallel ishlaydi
    await asyncio.gather(start_web_server(), start_bot())


if __name__ == "__main__":
    asyncio.run(main())

