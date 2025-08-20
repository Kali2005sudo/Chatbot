from __future__ import annotations
import json
from .config import MEM_FILE, MAX_HISTORY

DEFAULT = {
    "name": None,
    "city": None,
    "mood": "friendly",
    "reminders": [],
    "history": [],
    "voice_on": False,
    "last_topic": None,
    "last_weather": {},
}


def load():
    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            m = json.load(f)
    except Exception:
        m = {}
    for k, v in DEFAULT.items():
        m.setdefault(k, v)
    return m


def save(m):
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)


def append_history(M, user, corr, ts):
    M["history"].append({"ts": ts, "user": user, "corr": corr})
    if len(M["history"]) > MAX_HISTORY:
        M["history"].pop(0)
