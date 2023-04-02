import asyncio

from aiogram import Bot, Dispatcher

from bot import config  # Должен быть импортирован раньше moviepy
from bot.logger import logger
from bot.handlers import user
from bot.ui_commands import set_ui_commands
from bot.middlewares import DbSessionMiddleware
from bot.database import AsyncSessionmaker


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(AsyncSessionmaker))
    dp.include_router(user.router)

    await set_ui_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped!')
