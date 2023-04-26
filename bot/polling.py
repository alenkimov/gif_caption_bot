import asyncio

from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN  # Должен быть импортирован раньше moviepy
from bot.handlers import user
from bot.ui_commands import set_ui_commands
from bot.middlewares import DbSessionMiddleware
from bot.database import AsyncSessionmaker


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await set_ui_commands(bot)


def run_polling(skip_updates: bool = None):
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(AsyncSessionmaker))
    dp.include_router(user.router)
    dp.startup.register(on_startup)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.delete_webhook(drop_pending_updates=skip_updates))
    loop.run_until_complete(dp.start_polling(bot))
