from __future__ import annotations
import re
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from .utils import norm
from .config import TZ_NAME

TZ = ZoneInfo(TZ_NAME)
WD = {
    d: i
    for i, d in enumerate(
        "monday tuesday wednesday thursday friday saturday sunday".split()
    )
}


def _merge_time(text: str, base):
    m = re.search(r"(?:\bat\s*)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", text)
    if not m:
        return None
    h = int(m[1])
    mi = int(m[2] or 0)
    ap = (m[3] or "").lower()
    if ap:
        if h == 12:
            h = 0 if ap == "am" else 12
        elif ap == "pm":
            h += 12
    dt = base.replace(hour=h, minute=mi, second=0, microsecond=0)
    if dt < base:
        dt += timedelta(days=1)
    return dt


def parse_time(now_fn, text: str):
    t = norm(text)
    dt = now_fn()
    if m := re.search(r"\bin\s+(\d+)\s*(min|mins|minutes|hour|hours|day|days)\b", t):
        v = int(m[1])
        u = {"min": "minutes", "mins": "minutes"}.get(m[2], m[2])
        return dt + timedelta(**{u: v})
    if "tomorrow" in t:
        base = (dt + timedelta(days=1)).replace(second=0, microsecond=0)
        return _merge_time(t, base) or base.replace(hour=9, minute=0)
    if m := re.search(
        r"\bnext\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", t
    ):
        target = WD[m[1]]
        days = ((target - dt.weekday() + 7) % 7) or 7
        base = (dt + timedelta(days=days)).replace(second=0, microsecond=0)
        return _merge_time(t, base) or base.replace(hour=9, minute=0)
    return _merge_time(t, dt)


def clean_text(t: str):
    return re.sub(r"\b(at|in|tomorrow|next\s+\w+)\b.*", "", t, flags=re.I).strip(" ,.-")


def add_reminder(M, now_fn, raw: str):
    when = parse_time(now_fn, raw)
    r = {
        "text": clean_text(raw) or "Reminder",
        "time": when.isoformat() if when else None,
        "notified": False,
    }
    M["reminders"].append(r)
    return f"✅ '{r['text']}'" + (f" at {when.strftime('%a %I:%M %p')}" if when else "")


def list_reminders(M):
    R = M["reminders"]
    if not R:
        return "You have no reminders."
    out = [
        "#  | Text                         | Time         | Status",
        "---+------------------------------+--------------+--------",
    ]
    for i, r in enumerate(R, 1):
        t = (
            datetime.fromisoformat(r["time"]).astimezone(TZ).strftime("%a %I:%M %p")
            if r.get("time")
            else "—"
        )
        out.append(
            f"{i:>2} | {r['text'][:28]:<28} | {t:<12} | {'done' if r.get('notified') else 'pending'}"
        )
    return "\n".join(out)


def delete_reminder(M, i: int):
    R = M["reminders"]
    if 1 <= i <= len(R):
        x = R.pop(i - 1)
        return f"🗑️ Deleted '{x['text']}'"
    return "Invalid reminder number."


def mark_done(M, i: int):
    R = M["reminders"]
    if 1 <= i <= len(R):
        R[i - 1]["notified"] = True
        return f"✅ Marked done '{R[i-1]['text']}'"
    return "Invalid reminder number."


def due_msgs(M, now_fn):
    out = []
    t = now_fn()
    for r in M["reminders"]:
        if r.get("time") and not r.get("notified"):
            when = datetime.fromisoformat(r["time"])
            if when.tzinfo is None:
                when = when.replace(tzinfo=TZ)
            if t >= when:
                r["notified"] = True
                out.append(f"⏰ Reminder: {r['text']}")
    return out
