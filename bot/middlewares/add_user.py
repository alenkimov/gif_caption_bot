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
    """
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession = data['session']
        telegram_id = event.from_user.id
        username = event.from_user.username
        first_name = event.from_user.first_name
        last_name = event.from_user.last_name
        user = await session.scalar(select(User).filter_by(telegram_id=telegram_id))
        if user is None:
            user = User(telegram_id=telegram_id,
                        username=username,
                        first_name=first_name,
                        last_name=last_name)
            session.add(user)
        else:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
        await session.commit()
        data['user'] = user
        return await handler(event, data)
