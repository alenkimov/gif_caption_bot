from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.models import User


class AddUserMiddleware(BaseMiddleware):
    """
    Добавляет или обновляет данные о пользователе. Пробрасывает пользователя в хендлер.

    Если пользователя не существует — создает его.
    Если существует — обновляет его данные (имя пользователя, имя и фамилию).
    Пробрасывает пользователя в хендлер, чтобы не приходилось его заново запрашивать.

    Так как использует сессию базы данных, должен использоваться после DbSessionMiddleware.
    """
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession = data['session']
        user = User(telegram_id=event.from_user.id,
                    username=event.from_user.username,
                    first_name=event.from_user.first_name,
                    last_name=event.from_user.last_name)
        user = await session.merge(user)
        data['user'] = user
        return await handler(event, data)
