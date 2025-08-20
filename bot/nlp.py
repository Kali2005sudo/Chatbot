from __future__ import annotations
import re, math
from datetime import timedelta
from .utils import norm, tokens, has_like, fuzzy_ratio, pick, time_of_day, now
from . import memory
from . import fun, mathx, reminders, weather, voice
from .translator import translate

GREET_WORDS = ["hi", "hello", "hey", "salam", "assalam o alaikum", "hye", "hy"]


def greet(M):
    start = pick(
        "greet",
        [time_of_day() + "!", time_of_day() + ", friend!", time_of_day() + ", Shoaib!"],
    )
    tail = f"Nice to see you, {M['name']}" if M.get("name") else "Nice to see you."
    return f"{start} {tail}"


def reply(M, user_text: str):
    u = str(user_text)
    t = norm(u)

    # due reminders bubble up first
    dues = reminders.due_msgs(M, now)

    def add(s: str):
        return "\n".join(dues + [s]) if dues else s

    memory.append_history(M, u, u, now().isoformat(timespec="seconds"))

    # exits
    if re.search(r"\b(bye|exit|quit)\b", t):
        return add("👋 Goodbye!")

    # voice toggles / listen
    if "voice on" in t or has_like(t, "voice on"):
        return add(voice.toggle_voice(M, True))
    if "voice off" in t or has_like(t, "voice off"):
        return add(voice.toggle_voice(M, False))
    if re.search(r"\b(listen|hear me)\b", t):
        txt, err = voice.listen_once()
        return add(err) if err else add(f"I heard: {txt}")

    # greetings
    if any(fuzzy_ratio(tok, g) >= 70 for tok in tokens(u) for g in GREET_WORDS):
        return add(greet(M) + " How’s your day going?")

    # who/how
    if has_like(t, "who are you") or has_like(t, "what are you"):
        return add(
            "I'm CodeAlphaBot — math, facts, reminders, translate, weather and good vibes."
        )
    if has_like(t, "how are you"):
        return add(
            f"I'm {pick('how',['focused and ready!','sipping virtual chai ☕','energized and curious!'])} How are you?"
        )

    # mood
    if "set mood to" in t:
        for m in ["friendly", "funny", "sarcastic"]:
            if m in t:
                M["mood"] = m
                return add(f"Mood changed to {m}.")
        return add("Available moods: friendly, funny, sarcastic.")
    if has_like(t, "what is my mood") or has_like(t, "whats my mood"):
        return add(f"Your current mood is {M.get('mood','friendly')}")

    # emotions
    if any(
        p in t for p in ["i am sad", "feeling down", "depressed", "unhappy", "udaas"]
    ):
        return add(
            "I'm sorry you're feeling low. Want a joke, a gentle fact, or a tiny breathing tip?"
        )
    if any(p in t for p in ["i am happy", "feeling good", "excited", "great", "khush"]):
        return add("Yay! Love that energy! ✨")

    # fun
    if has_like(t, "riddle"):
        return add(fun.riddle())
    if has_like(t, "compliment"):
        return add(fun.compliment())
    if has_like(t, "fact"):
        return add(fun.fact())
    if has_like(t, "joke"):
        return add(fun.joke())
    if has_like(t, "coin") or has_like(t, "toss"):
        return add(
            f"The coin shows: {'Heads' if math.floor(math.pi*1000)%2==0 else 'Tails'}"
        )
    if has_like(t, "dice") or has_like(t, "die"):
        return add(f"🎲 You rolled a {math.floor(math.pi*1000)%6+1}")

    # date/time
    if has_like(t, "date"):
        return add(now().strftime("Today's date is %A, %B %d, %Y."))
    if has_like(t, "time"):
        return add(f"The current time is {now().strftime('%I:%M:%S %p')}")

    # math
    if (mv := mathx.math_verb(t)) is not None:
        return add(f"The result is {mv}")
    if re.search(r"\d|!", u) and any(
        x in u
        for x in [
            "+",
            "-",
            "*",
            "/",
            "^",
            "plus",
            "minus",
            "times",
            "divided",
            "mod",
            "!",
        ]
    ):
        try:
            return add(f"The result is {mathx.eval_expr(u)}")
        except Exception:
            pass
    if t.startswith("factorial"):
        m = re.search(r"-?\d+", u)
        if not m:
            return add("Use: factorial <non-negative integer> (e.g. factorial 5)")
        n = int(m.group())
        if n < 0:
            return add("Use: factorial <non-negative integer>")
        return add(f"The factorial of {n} is {math.factorial(n)}")
    if has_like(t, "square of"):
        m = re.search(r"-?\d+(\.\d+)?", u)
        return (
            add("Use: square of <number>")
            if not m
            else add(f"The square of {float(m.group())} is {float(m.group())**2}")
        )
    if has_like(t, "cube of"):
        m = re.search(r"-?\d+(\.\d+)?", u)
        return (
            add("Use: cube of <number>")
            if not m
            else add(f"The cube of {float(m.group())} is {float(m.group())**3}")
        )
    if has_like(t, "sqrt") or has_like(t, "square root of"):
        m = re.search(r"-?\d+(\.\d+)?", u)
        if not m:
            return add("Use: sqrt <number> or square root of <number>")
        x = float(m.group())
        return (
            add("Square root of negative number is not supported.")
            if x < 0
            else add(f"The square root of {x} is {round(x**0.5,6)}")
        )
    if t.startswith("power"):
        m = re.findall(r"-?\d+(?:\.\d+)?", u)
        return (
            add("Format: power <base> <exponent>")
            if len(m) < 2
            else add(f"{float(m[0])} ^ {float(m[1])} = {float(m[0])**float(m[1])}")
        )

    # conversions / table
    conv = mathx.conversions(u)
    if conv:
        return add(conv)
    if "table" in t:
        return add(mathx.table_cmd(u))

    # reminders
    if t.startswith("remind me") or "remind" in t:
        return add(reminders.add_reminder(M, now, u))
    if re.search(r"\b(show|list)\s+reminders\b", t):
        return add(reminders.list_reminders(M))
    if re.search(r"\b(clear|delete)\s+reminders\b", t):
        M["reminders"].clear()
        return add("All reminders cleared.")
    if m := re.search(r"\bdelete\s+reminder\s+(\d+)\b", t):
        return add(reminders.delete_reminder(M, int(m[1])))
    if m := re.search(r"\b(mark|complete)\s+reminder\s+(\d+)\b", t):
        return add(reminders.mark_done(M, int(m[2])))

    # name & city
    for pat in [
        r"\bmy name is\s+(\w+)",
        r"\bi am\s+(\w+)",
        r"\bi'm\s+(\w+)",
        r"\bthis is\s+(\w+)",
    ]:
        m = re.search(pat, u, flags=re.I)
        if m:
            M["name"] = m.group(1).capitalize()
            return add(f"Nice to meet you, {M['name']}! Where do you live?")
    if has_like(t, "what is my name") or has_like(t, "whats my name"):
        return add(f"Your name is {M.get('name','unknown')}.")
    if "i live in" in t or "i'm in" in t:
        part = (
            u.split("i live in", 1)[-1]
            if "i live in" in t
            else u.split("i'm in", 1)[-1]
        ).strip()
        city = part.split()[0].capitalize() if part else None
        if city:
            M["city"] = city
            return add(f"Cool! {city} sounds nice.")
        else:
            return add("Tell me your city after 'I live in'.")
    if "where" in t and "live" in t:
        return add(f"You told me you live in {M.get('city','an unknown city')}.")

    # memory commands
    if "clear memory" in t or "reset memory" in t:
        M.update(
            name=None,
            city=None,
            mood="friendly",
            reminders=[],
            history=[],
            last_topic=None,
        )
        return add("Memory cleared and mood reset.")
    if "show memory" in t:
        return add(
            f"Memory — name: {M.get('name') or 'unknown'}, city: {M.get('city') or 'unknown'}, mood: {M.get('mood') or 'friendly'}."
        )

    # help
    if "help" in t or "commands" in t:
        return add(
            "I handle: greetings, math, conversions, factorial/power/roots, tables, coin/dice, jokes/facts/riddles/compliments, reminders ('in 20 min', 'next Monday 7pm'), name/city, date/time. New: weather -> 'weather in <city>' | translate -> 'translate to ur <text>' or 'translate to en <text>' | Voice: 'voice on' / 'voice off' & 'listen'."
        )

    # weather & translate
    if m := re.search(r"\bweather(?:\s+in)?\s+([a-zA-Z\s]+)", u, flags=re.I):
        city = m.group(1).strip()
        M["last_topic"] = "weather"
        return add(weather.get_weather(M, city))
    if (
        "weather" in t
        and M.get("last_topic") == "weather"
        and re.match(r"^\s*and\s+", u.strip().lower())
    ):
        city = re.sub(r"^\s*and\s+", "", u.strip(), flags=re.I)
        return add(weather.get_weather(M, city))

    if m := re.search(r"\btranslate\s+(?:to\s+(\w+))\s+(.+)", u, flags=re.I):
        dest = (m.group(1) or "").lower()
        text = m.group(2).strip()
        dest_code = (
            "ur"
            if dest.startswith("ur") or dest == "urdu"
            else ("en" if dest.startswith("en") else dest)
        )
        return add(translate(text, dest=dest_code))
    if "translate" in t and ("to ur" in t or "to urdu" in t or "urdu" in t):
        parts = re.split(r"to\s+urdu", u, flags=re.I)
        if len(parts) > 1:
            return add(translate(parts[1].strip(), dest="ur"))

    # suggestions (friendly)
    return add(
        "Sorry, I didn't understand that 🤔. Try: 'show reminders', 'weather in Karachi', 'translate to ur Hello'. Type 'help' for more."
    )
