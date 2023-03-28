import secrets
from io import BytesIO
import os

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile, FSInputFile

from utils import watermarked_photo, watermarked_mp4
from definitions import TEMP_DIR

router = Router()


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'Отправь мне фото или гиф-анимацию '
                         f'и я добавлю вотермарку в виде твоего имени пользователя!')


@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    photo = BytesIO()
    await bot.download(message.photo[-1], destination=photo)
    telegram_handle = f'@{message.from_user.username}'
    if message.caption:
        watermark = message.caption
    else:
        watermark = telegram_handle
    with watermarked_photo(photo, watermark) as photo:
        buffered = BufferedInputFile(photo.getvalue(), 'watermarked.jpg')
        await message.reply_photo(buffered)


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
