from pathlib import Path
from os import makedirs

BASE_DIR = Path(__file__).resolve().parent.parent
DOT_ENV_FILEPATH = BASE_DIR / '.env'
TEMP_DIR = BASE_DIR / '.temp'
LOG_DIR = BASE_DIR / 'log'


makedirs(TEMP_DIR, exist_ok=True)
makedirs(LOG_DIR, exist_ok=True)
