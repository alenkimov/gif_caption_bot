from datetime import datetime

from sqlalchemy import String, BigInteger, SmallInteger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from aiogram import html

from bot.config import ALL_FONTS, DEFAULT_FONT


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = 'user'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32))
    first_name: Mapped[str | None] = mapped_column(String(120))
    last_name: Mapped[str | None] = mapped_column(String(120))
    animation_file_id: Mapped[str | None] = mapped_column(String(120))
    last_gif_created_at: Mapped[datetime | None]
    count_of_creations: Mapped[int] = mapped_column(default=0)
    font: Mapped[str] = mapped_column(String(120), default=DEFAULT_FONT)
    font_size: Mapped[int] = mapped_column(SmallInteger, default=36)
    font_color: Mapped[str] = mapped_column(String(60), default='white')
    stroke: Mapped[bool] = mapped_column(default=True)
    stroke_color: Mapped[str] = mapped_column(default='black')
    position: Mapped[str] = mapped_column(default='bottom')

    def __repr__(self):
        if self.username: return f'<User(telegram_id={self.telegram_id}, username={self.username}>'
        else: return f'<User(telegram_id={self.telegram_id}>'

    def get_name(self):
        if self.username:
            return f'@{self.username}'
        elif self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return f'{self.first_name}'
        else:
            return f'{self.telegram_id}'

    def get_info(self):
        """
        Возвращает информацию о пользователе.

        Пример:
        ```
        Привет, @AlenKimov!
        Твой Telegram ID: `0000000000`
        Количество созданных гифок: 266

        Настройки: /settings
        ```
        """
        parts = [
            f'Привет, {self.get_name()}!',
            f'Твой Telegram ID: {html.code(self.telegram_id)}',
            f'Количество созданных гифок: {self.count_of_creations}\n',
            f'Настройки: /settings',
        ]
        return '\n'.join(parts)

    def get_settings_info(self):
        """
        Возвращает информация о настройках пользователя.

        Пример:
        ```
        Settings:

        #     ┏━ Цвет шрифта
        #     ┃      ┏━ Размер шрифта
        #     ┃      ┃   ┏━ Шрифт
        Шрифт: white, 10% [ Calibri ]
        #       ┏━ Цвет обводки (если обводка включена)
        Обводка: black
        #          ┏━ Позиция
        Позиция: bottom
        ```
        """
        parts = [html.bold('Settings\n')]
        parts.append(f'Шрифт: {self.font_color}, {self.font_size} [ {self.font} ]')
        if self.stroke:
            parts.append(f'Обводка: {self.stroke_color}')
        parts.append(f'Позиция: {self.position}')
        return '\n'.join(parts)

    async def async_get_leaderboard_info(self, session: AsyncSession):
        """Возвращает информацию о таблице лидеров.

        Пример:
        ```
        Leaderboard

        [1] 266 — @AlenKimov
        [2] 059 — @AnotherUser1
        [3] 057 — @AnotherUser2
        [4] 056 — @AnotherUser3
        [5] 042 — Another User  # Имя пользователя не установлено
        [6] 037 — @AnotherUser5
        [7] 024 — @AnotherUser6
        [8] 011 — @AnotherUser7
        [9] 009 — @AnotherUser8
        ...
        [26] 002 — [ @AnotherUser9 ]
        ```
        """
        ordered_users = (await session.scalars(select(User).order_by(User.count_of_creations.desc()))).all()
        parts = [html.bold('Leaderboard')]

        this_user_number = ordered_users.index(self) + 1

        if this_user_number == 10: limit = 11
        else: limit = 10

        for index, user in enumerate(ordered_users[:limit]):
            number = index + 1
            if user is self: name = f'[ {user.get_name()} ]'
            else: name = user.get_name()
            parts.append(f'[{number}] {user.count_of_creations:03d} — {name}')

        if this_user_number > 10:
            parts.append('...')
            name = f'[ {self.get_name()} ]'
            parts.append(f'[{this_user_number}] {self.count_of_creations:03d} — {name}')

        return '\n'.join(parts)

    def get_fonts(self):
        """
        Возвращает список шрифтов.

        Пример:
        Пример вывода списка шрифтов:
        ```
        Fonts: 7

        Arial
         [ Calibri ]  # Этот шрифт установлен у пользователя
        Candara
        Comic-Sans-MS
        Consolas
        Constantia
        Corbel
        ```
        """
        parts = [html.bold(f'Fonts: {len(ALL_FONTS)}')]
        for font in ALL_FONTS:
            if font.lower() == self.font.lower(): parts.append(f'[ {font} ]')
            else: parts.append(font)
        return '\n'.join(parts)
