# GIF Caption Bot
Телеграм бот для добавления текста на гифку.

## Возможности бота
- Если отправить боту гифку, он добавит на нее имя пользователя отправителя (такого рода вотермарку).
- Если отправить боту гифку с подписью, он добавит на нее эту подпись.
- Если отредактировать подпись, бот отправит гифку с новой подписью.


## Запуск на Windows
1. Установите [Python 3.11.2](https://www.python.org/downloads/windows/). Не забудьте поставить галочку напротив "Add Python to PATH".
2. Установите пакетный менеджер [Poetry](https://python-poetry.org/docs/).
3. Установите [ImageMagick](https://imagemagick.org/script/download.php).
4. В файле `.env`:
	1. Установите `BOT_TOKEN`, взятый из [BotFather](https://t.me/BotFather).
	2. Установите `IMAGEMAGICK_BINARY` ([подробнее об этом](https://moviepy-tburrows13.readthedocs.io/en/improve-docs/install.html#custom-paths-to-external-tools)).
5. В папке проекта пропишите следующие команды:
```bash
poetry update
poetry run python -m bot
```