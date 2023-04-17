from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import (
    BOT_TOKEN,
    WEB_SERVER_HOST,
    WEB_SERVER_PORT,
    WEBHOOK_URL,
    WEBHOOK_PATH,
)  # Должен быть импортирован раньше moviepy
from bot.logger import logger
from bot.handlers import user
from bot.ui_commands import set_ui_commands
from bot.middlewares import DbSessionMiddleware
from bot.database import AsyncSessionmaker


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await set_ui_commands(bot)  # Setting UI commands


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


def main():
    # Bot and Dispatcher instances
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(AsyncSessionmaker))
    dp.include_router(user.router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Polling
    # await bot.delete_webhook(drop_pending_updates=True)
    # await dp.start_polling(bot)

    # Creating an aiohttp application
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

    # -- Does not work
    # runner = web.AppRunner(app)
    # await runner.setup()
    # site = web.TCPSite(runner, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    # await site.start()
    # await asyncio.Event().wait()


if __name__ == '__main__':
    try:
        main()
        # asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped!')
