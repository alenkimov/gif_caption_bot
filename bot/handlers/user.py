from datetime import datetime, timedelta
import secrets
import os

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import DELAY, ALL_FONTS_LOWER, ALL_COLORS, ALL_POSITIONS
from bot.utils import captioned_mp4
from bot.definitions import TEMP_DIR
from bot.middlewares import AddUserMiddleware
from bot.models import User
from bot.handlers.message_texts import START_MESSAGE_TEXT, HELP_MESSAGE_TEXT

router = Router()
router.message.middleware(AddUserMiddleware())
router.edited_message.middleware(AddUserMiddleware())


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(START_MESSAGE_TEXT, disable_web_page_preview=True)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(HELP_MESSAGE_TEXT, disable_web_page_preview=True)


@router.message(Command('me', 'my'))
async def cmd_me(message: Message, user: User):
    await message.answer(user.get_info())


@router.message(Command('settings', 'setting'))
async def cmd_settings(message: Message, user: User):
    await message.answer(user.get_settings_info())


@router.message(Command('leaderboard', 'board'))
async def cmd_leaderboard(message: Message, user: User, session: AsyncSession):
    await message.answer(await user.async_get_leaderboard_info(session))


@router.message(Command('font', 'fonts', magic=~F.args))
async def cmd_font(message: Message, user: User):
    await message.answer(user.get_fonts())


@router.message(Command('font', 'fonts', magic=F.args.cast(int).as_('font_size')))
async def cmd_font_size(message: Message, user: User, session: AsyncSession, font_size: int):
    if font_size > 100 or font_size < 1:
        await message.reply(f'Размер шрифта должен быть в пределах от 1% до 100%')
    else:
        user.font_size = font_size
        await session.commit()
        await message.reply(f'Размер шрифта установлен')


@router.message(Command('font', 'fonts', magic=F.args.cast(str).as_('font')))
async def cmd_font_name(message: Message, user: User, session: AsyncSession, font: str):
    if font.lower() not in ALL_FONTS_LOWER:
        await message.reply(f'Шрифт не найден. Доступные шрифты: /font')
    else:
        user.font = font
        await session.commit()
        await message.reply(f'Шрифт установлен')


@router.message(Command('font_color', magic=F.args.cast(str).as_('color')))
async def cmd_font_color(message: Message, user: User, session: AsyncSession, color: str):
    color = color.lower()
    if color not in ALL_COLORS:
        await message.reply(f'Цвет не найден. Доступные цвета: {", ".join(ALL_COLORS)}.')
    else:
        user.font_color = color
        await session.commit()
        await message.reply(f'Цвет шрифта установлен')


@router.message(Command('stroke'))
async def cmd_stroke(message: Message, user: User, session: AsyncSession):
    if user.stroke:
        user.stroke = False
        await message.reply(f'Обводка выключена')
    else:
        user.stroke = True
        await message.reply(f'Обводка включена\nЦвет обводки: {user.stroke_color}')
    await session.commit()


@router.message(Command('stroke_color', magic=F.args.cast(str).as_('color')))
async def cmd_stroke_color(message: Message, user: User, session: AsyncSession, color: str):
    color = color.lower()
    if color not in ALL_COLORS:
        await message.reply(f'Цвет не найден. Доступные цвета: {", ".join(ALL_COLORS)}.')
    else:
        user.stroke_color = color
        await session.commit()
        await message.reply(f'Цвет обводки установлен')


@router.message(Command('position', magic=F.args.cast(str).as_('position')))
async def cmd_position(message: Message, user: User, session: AsyncSession, position: str):
    position = position.lower()
    if position not in ALL_POSITIONS:
        await message.reply(f'Неизвестная позиция. Доступные позиции: {", ".join(ALL_POSITIONS)}.')
    else:
        user.position = position
        await session.commit()
        await message.reply(f'Позиция текста установлена')


async def create_gif_and_answer(message: Message, user: User, bot: Bot):
    """
    Скачивает последнюю отправленную пользователем гифку и добавляет на нее текст этого сообщения.

    Подпись на гифку можно добавлять не чаще определенного времени (bot.config.DELAY).
    """
    if user.animation_file_id is None:
        return
    now = datetime.utcnow()
    delta = timedelta(seconds=DELAY)
    delay_ago = now - delta
    if user.last_gif_created_at is not None and user.last_gif_created_at > delay_ago:
        seconds_left = ((user.last_gif_created_at + delta) - now).seconds
        await message.reply(f'Wait {seconds_left} seconds!')
    else:
        user.last_gif_created_at = now
        user.count_of_creations += 1
        mp4_filepath = TEMP_DIR / f'{user.username}-{secrets.token_urlsafe(8)}.mp4'
        await bot.download(user.animation_file_id, destination=mp4_filepath)
        kwargs = {
            'font': user.font,
            'font_size': user.font_size,
            'font_color': user.font_color,
            'stroke': user.stroke,
            'stroke_color': user.stroke_color,
            'position': user.position,
        }
        with captioned_mp4(mp4_filepath, user.last_caption, **kwargs) as watermarked_mp4_filename:
            await message.reply_animation(FSInputFile(watermarked_mp4_filename))
        os.remove(mp4_filepath)


@router.message(Command('repeat', 'again', 'r'))
async def cmd_repeat(message: Message, user: User, session: AsyncSession, bot: Bot):
    if user.last_caption is None:
        return
    await create_gif_and_answer(message, user, bot)
    await session.commit()


@router.message(F.animation)
async def animation_handler(message: Message, user: User, session: AsyncSession):
    user.animation_file_id = message.animation.file_id
    await session.commit()


@router.message(F.text)
@router.edited_message(F.text)
async def text_handler(message: Message, user: User, session: AsyncSession, bot: Bot):
    user.last_caption = message.text
    await create_gif_and_answer(message, user, bot)
    await session.commit()
