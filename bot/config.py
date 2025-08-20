from __future__ import annotations
from pathlib import Path
import os

# Files/paths
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
MEM_FILE = DATA_DIR / "bot_memory.json"

# Timezone
TZ_NAME = "Asia/Karachi"

# API Keys (env preferred)
OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY", "8a4017c6a83964032ebfcf724bfdf787"
)

# Feature flags
TYPING_DELAY = 0.0  # 0 for instant, tweak if you want typing effect
MAX_HISTORY = 200
