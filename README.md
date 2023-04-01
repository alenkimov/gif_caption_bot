# GIF Caption Bot
Телеграм бот для добавления текста на гифку.

## Возможности бота
- Если отправить боту гифку, он добавит на нее имя пользователя отправителя (такого рода вотермарку).
- Если отправить боту гифку с подписью, он добавит на нее эту подпись.
- Если отредактировать подпись, бот отправит гифку с новой подписью.

## Установка и запуск под Windows
1. Установите [Python 3.11](https://www.python.org/downloads/windows/). Не забудьте поставить галочку напротив "Add Python to PATH".
2. Установите пакетный менеджер [Poetry](https://python-poetry.org/docs/).
3. Установите [ImageMagick](https://imagemagick.org/script/download.php).
4. Скачайте или склонируйте папку проекта, после чего перейдите в нее:
   - Создайте и заполните `.env`-файл (инструкция ниже).
   - Пропишите следующие команды:
   ```bash
   poetry update
   poetry run python -m bot
   ```
5. Создайте в корне проекта файл `.env`.
   - Зарегестрируйте Telegram бота через [@BotFather](https://t.me/BotFather) и присвойте полученный токен переменной `BOT_TOKEN`.
   - Присвойте переменной `IMAGEMAGICK_BINARY` путь до исполняемого файла `magick.exe` ([подробнее об этом](https://moviepy-tburrows13.readthedocs.io/en/improve-docs/install.html#custom-paths-to-external-tools)).
     Пример `.env` файла:
   ```
   BOT_TOKEN=0000000000:AaBbCcDdEeFfGgHhIiJjKkLlMmNn
   IMAGEMAGICK_BINARY=C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe
   ```

## Установка и запуск под Ubuntu
1. Обновите систему, установите screen, [git](https://git-scm.com/download/linux) и [ImageMagick](https://imagemagick.org/script/install-source.php#linux):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install screen git imagemagick -y
screen --version
git --version

```
2. Установите Python 3.11:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 -y
ln -s /usr/bin/python3.11 /usr/bin/python
python --version
```
3. Установите [Poetry](https://python-poetry.org/docs/):
```bash
curl -sSL https://install.python-poetry.org | python -
export PATH="/root/.local/bin:$PATH"
poetry --version
```
4. Склонируйте этот репозиторий и перейдите в папку проекта:
```bash
git clone https://github.com/AlenKimov/gif_caption_bot.git
cd gif_caption_bot
```
5. Создайте в корне проекта файл `.env`:
   - Зарегестрируйте Telegram бота через [@BotFather](https://t.me/BotFather) и присвойте полученный токен переменной `BOT_TOKEN`.
   Пример `.env` файла:
   ```
   BOT_TOKEN=0000000000:AaBbCcDdEeFfGgHhIiJjKkLlMmNn
   ```
6. Для корректной работы ImageMagick ([подробнее](https://github.com/Zulko/moviepy/issues/401#issuecomment-278679961)) нужно отредактировать файл `/etc/ImageMagick-6/policy.xml`. Удалите следующую строку в конце файла:
```xml
<policy domain="path" rights="none" pattern="@*" />
```
Поскольку это xml, вы можете закомментировать эту строку следующим образом:
```xml
<!-- <policy domain="path" rights="none" pattern="@*" /> -->
```