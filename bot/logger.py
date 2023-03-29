"""Настройка логера Loguru"""
from datetime import datetime
import logging
import sys

from loguru import logger

from bot.definitions import LOG_DIR


DEBUG = True

FILE_LOG_FORMAT = "<white>{time:YYYY-MM-DD HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"
CONSOLE_LOG_FORMAT = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR:    "ERROR",
        logging.WARNING:  "WARNING",
        logging.INFO:     "INFO",
        logging.DEBUG:    "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup(debug: bool):
    logger.remove()
    log_file_name = f'{datetime.now().strftime("%d-%m-%Y")}.log'
    log_file_path = LOG_DIR / log_file_name
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.add(log_file_path, format=FILE_LOG_FORMAT, level="DEBUG", rotation='1 day')
    logger.add(sys.stderr, colorize=True, format=CONSOLE_LOG_FORMAT, level='DEBUG' if debug else 'INFO')


setup(DEBUG)
