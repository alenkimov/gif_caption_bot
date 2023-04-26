"""Настройка логера Loguru"""
import logging
import sys

from loguru import logger

from bot.config import LOGGING_LEVEL


CONSOLE_LOG_FORMAT = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: 'CRITICAL',
        logging.ERROR: 'ERROR',
        logging.WARNING: 'WARNING',
        logging.INFO: 'INFO',
        logging.DEBUG: 'DEBUG',
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup(level='DEBUG'):
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.remove()
    logger.add(sys.stderr, colorize=True, format=CONSOLE_LOG_FORMAT, level=level)
    logger.disable('sqlalchemy.engine.base')


setup(LOGGING_LEVEL)
