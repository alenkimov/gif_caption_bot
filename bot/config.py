import os

from dotenv import load_dotenv

from bot.definitions import DOT_ENV_FILEPATH


load_dotenv(DOT_ENV_FILEPATH)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'auto-detect')


from moviepy import config_defaults as moviepy_config_defaults
moviepy_config_defaults.IMAGEMAGICK_BINARY = IMAGEMAGICK_BINARY

from moviepy.video.VideoClip import TextClip

ALL_FONTS = TextClip.list('font')
ALL_FONTS_LOWER = [font.lower() for font in ALL_FONTS]

if 'Impact' in ALL_FONTS:
    DEFAULT_FONT = 'Impact'
else:
    DEFAULT_FONT = ALL_FONTS[0]

DELAY = int(os.getenv('DELAY', 30))
ALL_COLORS = ['white', 'black']
