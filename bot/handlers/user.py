import secrets
import os

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from utils import watermarked_mp4
from definitions import TEMP_DIR

router = Router()


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'Отправь мне гифку и я добавлю на нее твое имя пользователя!\n'
                         f'Или отправь мне гифку с подписью!')


@router.message(F.animation)
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
