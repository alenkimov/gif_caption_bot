import secrets

from decouple import Config, RepositoryEnv

from bot.paths import DOT_ENV_FILEPATH


env = Config(RepositoryEnv(DOT_ENV_FILEPATH))


BOT_TOKEN = env('BOT_TOKEN')

# Webhook
DOMAIN: str = env('DOMAIN')
DOMAIN = DOMAIN.rstrip('/')
DOMAIN = DOMAIN.lstrip('https://')
SECRET_KEY = secrets.token_urlsafe(48)
WEBHOOK_BASE_PATH = env('WEBHOOK_BASE_PATH', default='/webhook')
WEBHOOK_PATH = f'{WEBHOOK_BASE_PATH}/{SECRET_KEY}'
WEBHOOK_URL = f'https://{DOMAIN}{WEBHOOK_PATH}'
WEB_SERVER_HOST = env('WEB_SERVER_HOST', default='localhost')
WEB_SERVER_PORT = env('BOT_PUBLIC_PORT', default=8080, cast=int)
print(WEBHOOK_URL)

# Доступ к базе данных PostgreSQL
POSTGRES_HOST = env('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = env('POSTGRES_PORT', default=5432, cast=int)
POSTGRES_USER = env('POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD', default='')
POSTGRES_DB = env('POSTGRES_DB', default='gif_caption_bot')
POSTGRES_URI = f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Другие настройки
DELAY = env('DELAY', default=30, cast=int)  # Задержка на создание анимации для пользователя
MAX_WORKERS = env('MAX_WORKERS', default=10, cast=int)  # Максимальное количество процессов для обработки видео

# -- moviepy
ALL_COLORS = ['white', 'black']
ALL_POSITIONS = ['bottom', 'center', 'top']

# For linux users, 'convert' should be fine.
# For Windows users, you must specify the path to the ImageMagick
# 'magick' binary. For instance:
#     IMAGEMAGICK_BINARY=C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe
IMAGEMAGICK_BINARY = env('IMAGEMAGICK_BINARY', default='auto-detect')

from moviepy import config_defaults as moviepy_config_defaults
moviepy_config_defaults.IMAGEMAGICK_BINARY = IMAGEMAGICK_BINARY

from moviepy.video.VideoClip import TextClip

ALL_FONTS = TextClip.list('font')
ALL_FONTS_LOWER = [font.lower() for font in ALL_FONTS]

if 'Impact' in ALL_FONTS:
    DEFAULT_FONT = 'Impact'
else:
    DEFAULT_FONT = ALL_FONTS[0]


