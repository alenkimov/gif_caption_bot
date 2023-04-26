from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOT_ENV_FILEPATH = BASE_DIR / '.env'
TEMP_DIR = BASE_DIR / '.temp_mp4'

TEMP_DIR.mkdir(exist_ok=True)
