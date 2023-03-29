from pydantic import BaseSettings
from moviepy import config_defaults as moviepy_config_defaults

from bot.definitions import DOT_ENV_FILEPATH


class Settings(BaseSettings):
    BOT_TOKEN: str
    IMAGEMAGICK_BINARY: str = 'auto-detect'

    class Config:
        env_file = DOT_ENV_FILEPATH
        env_file_encoding = 'utf-8'


config = Settings()
moviepy_config_defaults.IMAGEMAGICK_BINARY = config.IMAGEMAGICK_BINARY
