from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    """
    Sets bot commands in UI
    :param bot: Bot instance
    """
    commands = [
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="me", description="Обо мне"),
        BotCommand(command="settings", description="Установленные настройки"),
        BotCommand(command="leaderboard", description="Таблица лидеров"),
        BotCommand(command="font", description="Список доступных шрифтов, установка шрифта и его размера"),
        BotCommand(command="font_color", description="Установка цвета шрифта."),
        BotCommand(command="position", description="Установка позиции текста"),
        BotCommand(command="stroke", description="Вкл/Выкл обводку."),
        BotCommand(command="stroke_color", description="Установка цвета обводки."),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )
