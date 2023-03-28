import asyncio

from aiogram import Bot, Dispatcher

from logger import logger
from config import config
from handlers import user
from ui_commands import set_ui_commands


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')

    dp = Dispatcher()
    dp.include_router(user.router)

    await set_ui_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped!')
