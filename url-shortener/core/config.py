from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URL_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"
