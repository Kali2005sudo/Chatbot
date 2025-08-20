from __future__ import annotations
import re, random, difflib
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Callable, Iterable
from .config import TYPING_DELAY, TZ_NAME

# Optional imports (ignore type warnings in editors)
try:
    from rapidfuzz import fuzz  # type: ignore[import-not-found]
except Exception:
    fuzz = None

TZ = ZoneInfo(TZ_NAME)
now = lambda: datetime.now(TZ)


def norm(s: str) -> str:
    return re.sub(r"[^\w\s:!']", "", (s or "").lower())


def tokens(s: str):
    return re.findall(r"[a-z]+", (s or "").lower())


def fuzzy_ratio(a: str, b: str) -> float:
    a, b = a or "", b or ""
    if fuzz:
        try:
            return float(fuzz.ratio(a, b))
        except Exception:
            pass
    return difflib.SequenceMatcher(None, a, b).ratio() * 100.0


def dynamic_threshold(a: str, b: str) -> int:
    L = max(len(a or ""), len(b or ""))
    if L <= 3:
        return 60
    if L <= 7:
        return 70
    return 82


def has_like(s: str, tgt: str, cut: int | None = None) -> bool:
    s, tgt = (s or "").lower(), (tgt or "").lower()
    cut = cut or dynamic_threshold(s, tgt)
    for t in tokens(s):
        if fuzzy_ratio(t, tgt) >= cut:
            return True
    return fuzzy_ratio(s, tgt) >= cut


def pick(key: str, opts: list[str]) -> str:
    if not hasattr(pick, "_last"):
        pick._last = {}
    i = pick._last.get(key, -1)
    j = random.randrange(len(opts))
    if len(opts) > 1 and j == i:
        j = (j + 1) % len(opts)
    pick._last[key] = j
    return opts[j]


def time_of_day() -> str:
    h = now().hour
    if 5 <= h < 12:
        return "Good morning"
    if 12 <= h < 17:
        return "Good afternoon"
    if 17 <= h < 22:
        return "Good evening"
    return "Hey night owl"


def add_placeholder(entry, placeholder="Type your message..."):
    entry.delete(0, "end")
    entry.insert(0, placeholder)
    entry.config(fg="#d1d5db", insertontime=0)  # Light grey, clearly visible on dark bg

    def on_focus_in(e):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="#ffffff", insertontime=600)  # White text for user

    def on_focus_out(e):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="#d1d5db", insertontime=0)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
