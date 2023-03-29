import secrets
import os

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, Update

from bot.utils import watermarked_mp4
from bot.definitions import TEMP_DIR

router = Router()


HELP_MESSAGE_TEXT = """
Отправь мне гифку и я добавлю на нее твое имя пользователя!
Или отправь мне гифку с подписью и я добавлю на нее подпись!
Отредактируй подпись и я отправлю тебе новую гифку!
"""


@router.message(Command('help', 'start'))
async def cmd_help(message: Message):
    await message.answer(HELP_MESSAGE_TEXT)


@router.message(F.animation)
@router.edited_message(F.animation)
async def photo_handler(message: Message, bot: Bot):
    telegram_handle = f'@{message.from_user.username}'
    mp4_filepath = TEMP_DIR / f'{telegram_handle}-{secrets.token_urlsafe(8)}.mp4'
    await bot.download(message.animation, destination=mp4_filepath)
    if message.caption:
        watermark = message.caption
    else:
        watermark = telegram_handle
    with watermarked_mp4(mp4_filepath, watermark) as watermarked_mp4_filename:
        await message.reply_animation(FSInputFile(watermarked_mp4_filename))
    os.remove(mp4_filepath)
