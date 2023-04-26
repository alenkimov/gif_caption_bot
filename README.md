# GIF Caption Bot
Телеграм бот для добавления текста (подписи) на гифку.
[ [Ссылка на бота](https://t.me/gif_caption_bot) ]

## Подготовка к запуску под Windows
- Установите [Python 3.11](https://www.python.org/downloads/windows/). Не забудьте поставить галочку напротив "Add Python to PATH".
- Установите пакетный менеджер [Poetry](https://python-poetry.org/docs/) и [ImageMagick](https://imagemagick.org/script/download.php).
- [Скачайте](https://github.com/AlenKimov/gif_caption_bot/archive/refs/heads/main.zip) или склонируйте (если установлен [git](https://git-scm.com/download/win)) этот репозиторий, после чего перейдите в него:
```bash
git clone https://github.com/AlenKimov/gif_caption_bot.git
cd gif_caption_bot
```

## Подготовка к запуску под Ubuntu
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
- Установите PostgreSQL, задайте пароль учетной записи "postgres" и создайте базу данных (лучше делать это в новом терминале):
```bash
sudo apt install postgresql postgresql-contrib -y
sudo passwd postgres
sudo -i -u postgres
createdb gif_caption_bot
psql
\password
\q
```
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

## Наполнение `.env` файла
> Если значение переменной не задано, то будет задано значение по умолчанию, если такое имеется.
> Переменные без значения по умолчанию должны быть заданы обязательно.

- Зарегистрируйте Telegram бота через [@BotFather](https://t.me/BotFather) и присвойте переменной `BOT_TOKEN` 
  полученный токен.
- (Только при использовании webhook) Задайте следующие переменные:
  - `DOMAIN`. По умолчанию: example.com
  - `WEBHOOK_BASE_PATH`. По умолчанию: webhook
  - `WEB_SERVER_HOST`. Хост по умолчанию: localhost
  - `WEB_SERVER_PORT`. Порт по умолчанию: 8080
- Задайте переменные для доступа к базе данных PostgreSQL: 
  - `POSTGRES_HOST`. Хост по умолчанию: localhost
  - `POSTGRES_PORT`. Порт по умолчанию: 5432
  - `POSTGRES_USER`. Имя пользователя по умолчанию: postgres
  - `POSTGRES_PASSWORD`. Пароль по умолчанию: postgres
  - `POSTGRES_DB`. Название базы данных по умолчанию: gif_caption_bot
- Присвойте переменной `DELAY` желаемую задержку на запросы на создание анимации в секундах. 
Задержка по умолчанию: 30 секунд.
- Присвойте переменной `MAX_WORKERS` максимальное количество процессов для обработки видео.
- (Только для Windows) Присвойте переменной `IMAGEMAGICK_BINARY` путь до исполняемого файла `magick.exe` ([подробнее об 
  этом](https://moviepy-tburrows13.readthedocs.io/en/improve-docs/install.html#custom-paths-to-external-tools)).

Пример `.env` файла:
  ```
  BOT_TOKEN=903276830:AAFgbkhvzmQJjc1286qDdtRZ8C7aA_GzDHA
  
  DOMAIN=https://3he5-128-78-1-120.ngrok-free.app
  WEB_SERVER_HOST=localhost
  WEB_SERVER_PORT=8080
  
  POSTGRES_HOST=localhost
  POSTGRES_PORT=5432
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_DB=gif_caption_bot
  
  DELAY=30
  MAX_WORKERS=10
  
  IMAGEMAGICK_BINARY=C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe
  ```

## Запуска бота
- Следующие команды установят требуемые библиотеки, создадут таблички в базе данных:
```bash
poetry update                
poetry run alembic upgrade head
```
- Запуск бота (поллинг):
```bash
poetry run python start.py polling --skip-updates
```
- Запуск бота (вебхук):
```bash
poetry run python start.py webhook
```

## О боте
Чтобы добавить подпись на гифку, нужно отправить боту гифку, затем нужно отправить саму подпись.

### Команды бота
- `/start` — Выводит приветственное сообщение с описанием возможностей бота.
- `/help` — Выводит список всех команд с описанием.
- `/me` | `/my` — Выводит информацию о пользователе.
- `/repeat` | `/r` | `/again` - Повторяет последний запрос.
- `/settings` — Выводит информацию о настройках пользователя.
- `/leaderboard` — Выводит таблицу лидеров.
- `/font` — Выводит список доступных шрифтов и их количество. Установленный в данный момент шрифт будет отмечен в списке.
- `/font [font]` — Устанавливает указанный шрифт.
- `/font [font_size]` — Устанавливает указанный размер шрифта.
- `/font_color [color]` — Устанавливает указанный цвет шрифта.
- `/stroke` — Включает или отключает обводку.
- `/stroke_color [color]` — Устанавливает цвет обводки.
- `/position` — Меняет позицию текста на противоположную.

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

| Поле                           | Описание                               |
|--------------------------------|----------------------------------------|
| _telegram_id_ (Первичный ключ) | Telegram ID                            |
| _username_                     | Имя пользователя (username)            |
| _first_name_                   | Имя                                    |
| _last_name_                    | Фамилия                                |
| _animation_file_id_            | ID анимации                            |
| _last_gif_created_at_          | Дата и время последнего создания гифки |
| _count_of_creations_           | Количество созданных гифок             |
| _last_caption_                 | Последний запрос                       |
| _font_                         | Шрифт                                  |
| _font_size_                    | Размер шрифта                          |
| _font_color_                   | Цвет текста                            |
| _stroke_                       | Выполнять обводку текста?              |
| _stroke_color_                 | Цвет обводки                           |
| _position_                     | Позиция текста                         |
