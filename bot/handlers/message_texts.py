from aiogram import html

from bot.config import ALL_COLORS

GITHUB_LINK = 'https://github.com/AlenKimov/gif_caption_bot'
AUTHOR_LINK = 'https://t.me/AlenKimov'
CHANNEL_LINK = 'https://t.me/Cum_Insider'

LINKS_TEXT = html.bold(f'[ {html.link("GitHub", GITHUB_LINK)} | {html.link("Author", AUTHOR_LINK)} | {html.link("Channel", CHANNEL_LINK)} ]')

START_MESSAGE_TEXT = f"""
{LINKS_TEXT}

Чтобы добавить подпись на гифку, нужно отправь мне гифку, затем отправить саму подпись!
Отредактируй сообщение или отправь новое и я отправлю тебе новую гифку!

Подробнее о возможностях бота: /help
"""
HELP_MESSAGE_TEXT = f"""
{LINKS_TEXT}

Чтобы добавить подпись на гифку, нужно отправить боту гифку, затем нужно отправить саму подпись. Подпись можно отправлять раз в 30 секунд.

/me | /my — Выводит информацию о пользователе.
/settings — Выводит информацию о настройках пользователя.
/leaderboard — Выводит таблицу лидеров.
/font — Выводит список доступных шрифтов. Установленный в данный момент шрифт будет отмечен в списке.
/font [font] — Устанавливает указанный шрифт.
/font [font_size] — Устанавливает указанный размер шрифта.
/font_color [color] — Устанавливает указанный цвет шрифта.
/stroke — Включает или отключает обводку.
/stroke_color [color] — Устанавливает цвет обводки.
/position — Меняет позицию текста на противоположную.
/transition — Включает и отключает автоматический перенос текста на новую строку.

Доступные цвета [color]: {', '.join(ALL_COLORS)}.
Размер шрифта [font_size] может быть в пределах от 1% до 100%.
"""