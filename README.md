# GIF Caption Bot
Телеграм бот для добавления текста (подписи) на гифку.

## Установка и запуск под Windows
- Установите [Python 3.11](https://www.python.org/downloads/windows/). Не забудьте поставить галочку напротив "Add Python to PATH".
- Установите пакетный менеджер [Poetry](https://python-poetry.org/docs/) и [ImageMagick](https://imagemagick.org/script/download.php).
- [Скачайте](https://github.com/AlenKimov/gif_caption_bot/archive/refs/heads/main.zip) или склонируйте (если установлен [git](https://git-scm.com/download/win)) этот репозиторий, после чего перейдите в него:
```bash
git clone https://github.com/AlenKimov/gif_caption_bot.git
cd gif_caption_bot
```
- Создайте файл `.env` и заполните следующим образом:
   - Зарегистрируйте Telegram бота через [@BotFather](https://t.me/BotFather) и присвойте полученный токен переменной `BOT_TOKEN`.
   - Присвойте переменной `DATABASE_URL` ссылку на базу данных PostgreSQL следующего формата: `postgresql+psycopg://user:password@server/db`.
   - Присвойте переменной `IMAGEMAGICK_BINARY` путь до исполняемого файла `magick.exe` ([подробнее об этом](https://moviepy-tburrows13.readthedocs.io/en/improve-docs/install.html#custom-paths-to-external-tools)).
   - Пример `.env` файла:
     ```
     BOT_TOKEN=0000000000:AaBbCcDdEeFfGgHhIiJjKkLlMmNn
     DATABASE_URL=postgresql+psycopg://postgres:passw0rd@localhost/gif_caption_bot_database
     IMAGEMAGICK_BINARY=C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe
     ```
- Следующие команды установят требуемые библиотеки, создадут таблички в базе данных и запустят бота:
```bash
poetry update                
poetry run alembic upgrade head
poetry run python -m bot
```

## Установка и запуск под Ubuntu
- Обновите систему, установите шрифты, [git](https://git-scm.com/download/linux) и [ImageMagick](https://imagemagick.org/script/install-source.php#linux):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install screen git imagemagick ttf-mscorefonts-installer -y
```
- Для корректной работы ImageMagick ([подробнее](https://github.com/Zulko/moviepy/issues/401#issuecomment-278679961)) нужно отредактировать файл `/etc/ImageMagick-6/policy.xml`. Удалите следующую строку в конце файла:
```xml
<policy domain="path" rights="none" pattern="@*" />
```
Поскольку это xml, вы можете закомментировать эту строку следующим образом:
```xml
<!-- <policy domain="path" rights="none" pattern="@*" /> -->
```
- [Установите PostgreSQL и создайте базу данных](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04-ru#1-postgresql).
- Установите Python 3.11:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 -y
ln -s /usr/bin/python3.11 /usr/bin/python
```
- Установите [Poetry](https://python-poetry.org/docs/):
```bash
curl -sSL https://install.python-poetry.org | python -
export PATH="/root/.local/bin:$PATH"
```
- Склонируйте этот репозиторий, после чего перейдите в него:
```bash
git clone https://github.com/AlenKimov/gif_caption_bot.git
cd gif_caption_bot
```
- Создайте файл `.env` и заполните следующим образом:
   - Зарегистрируйте Telegram бота через [@BotFather](https://t.me/BotFather) и присвойте полученный токен переменной `BOT_TOKEN`.
   - Присвойте переменной `DATABASE_URL` ссылку на базу данных PostgreSQL следующего формата: `postgresql+psycopg://user:password@server/db`.
   - Пример `.env` файла:
     ```
     BOT_TOKEN=0000000000:AaBbCcDdEeFfGgHhIiJjKkLlMmNn
     DATABASE_URL=postgresql+psycopg://postgres:passw0rd@localhost/gif_caption_bot_database
     ```
- Следующие команды установят требуемые библиотеки, создадут таблички в базе данных и запустят бота:
```bash
poetry update                
poetry run alembic upgrade head
poetry run python -m bot
```

## О боте
Чтобы добавить подпись на гифку, нужно отправить боту гифку, затем нужно отправить саму подпись. 
Подпись можно отправлять не чаще определенного времени. По умолчанию оно равно 30 секундам. 
Это время изменить в переменных окружениях (`.env`), задав его переменной `DELAY`. Например:
```
DELAY=10
```
Изменения вступят в силу после перезагрузки бота.

### Команды бота
- `/start` — Выводит приветственное сообщение с описанием возможностей бота.
- `/help` — Выводит список всех команд с описанием.
- `/me` | `/my` — Выводит информацию о пользователе.
- `/settings` — Выводит информацию о настройках пользователя.
- `/leaderboard` — Выводит таблицу лидеров.
- `/font` — Выводит список доступных шрифтов и их количество. Установленный в данный момент шрифт будет отмечен в списке.
- `/font [font]` — Устанавливает указанный шрифт.
- `/font [font_size]` — Устанавливает указанный размер шрифта в процентах.*
- `/font_color [color]` — Устанавливает указанный цвет шрифта.
- `/stroke` — Включает или отключает обводку.
- `/stroke_color [color]` — Устанавливает цвет обводки.
- `/position` — Меняет позицию текста на противоположную.
- `/transition` — Включает и отключает автоматический перенос текста на новую строку.

*Размер шрифта может быть в пределах от 1 до 100 процентов. Это процент от 9/10 ширины гифки. По умолчанию — 10%. Это значит, что в одну строку поместется 9 букв.

### Информация о пользователе
Пример вывода информации о пользователе с установленным именем пользователя:
```
Привет, @AlenKimov!
Твой Telegram ID: `0000000000`
Количество созданных гифок: 266

Настройки: /settings
```

### Информация о настройках пользователя
Пример вывода информации о настройках пользователя:
```yaml
Settings

#     ┏━ Цвет шрифта
#     ┃      ┏━ Размер шрифта
#     ┃      ┃   ┏━ Шрифт
font: white, 10 [ Calibri ]
#       ┏━ Цвет обводки (если обводка включена)
stroke: black
#          ┏━ Позиция
position: bottom
#           ┏━ Перенос текста на новую строку
transition: false
```


### Таблица лидеров
Примеры таблицы лидеров:
```yaml
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

```yaml
Leaderboard
[1] 266 — [ @AlenKimov ]
[2] 059 — @AnotherUser1
[3] 057 — @AnotherUser2
[4] 056 — @AnotherUser3
[5] 042 — Another User
[6] 037 — @AnotherUser5
[7] 024 — @AnotherUser6
[8] 011 — @AnotherUser7
[9] 009 — @AnotherUser8
```

### Список шрифтов
Бот подтягивет шрифты системы.

Пример вывода списка шрифтов:
```yaml
Fonts: 7

Arial
 [ Calibri ]  # Этот шрифт установлен у пользователя
Candara
Comic-Sans-MS
Consolas
Constantia
Corbel
```

## База данных

[**user**]

| Поле                           | Описание                                 |
| ------------------------------ | ---------------------------------------- |
| _telegram_id_ (Первичный ключ) | Telegram ID                              |
| _username_                     | Имя пользователя (username)              |
| _first_name_                   | Имя                                      |
| _last_name_                    | Фамилия                                  |
| _animation_file_id_            | ID анимации                              |
| _last_gif_created_at_          | Дата и время последнего создания гифки   |
| _count_of_creations_           | Количество созданных пользователем гифок |
| _font_                         | Шрифт                                    |
| _font_size_                    | Размер шрифта                            |
| _font_color_                   | Цвет текста                              |
| _stroke_                       | Выполнять обводку текста?                |
| _stroke_color_                 | Цвет обводки                             |
| _position_                     | Позиция текста: сверху или снизу         |
| _transition_                   | Переносить текста на новую строку?       |
