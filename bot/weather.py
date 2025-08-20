from __future__ import annotations
from .config import OPENWEATHER_API_KEY
from .utils import now
import requests


def get_weather(M, city: str | None, target_time: str | None = None):
    if not city:
        city = M.get("city")
        if not city:
            return "Please say: weather in <city> (I can remember it)."
    if not OPENWEATHER_API_KEY:
        return "Weather API key missing."

    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url, timeout=6)
        data = r.json()
        if r.status_code != 200:
            return f"Weather API error: {data.get('message','unknown')}"

        cityname = data["city"]["name"]

        # ✅ Agar target_time na diya ho → current weather
        if not target_time:
            current = data["list"][0]
            desc = current["weather"][0]["description"].capitalize()
            temp = current["main"]["temp"]
            feels = current["main"]["feels_like"]
            hum = current["main"]["humidity"]
            return f"Weather in {cityname}: {desc}. Temp {temp}°C (feels {feels}°C). Humidity {hum}%."

        # ✅ Agar target_time diya ho → forecast search
        target_time = target_time.strip().lower()
        for forecast in data["list"]:
            dt_txt = forecast["dt_txt"].lower()
            if target_time in dt_txt:  # flexible match (date/time substring)
                desc = forecast["weather"][0]["description"].capitalize()
                temp = forecast["main"]["temp"]
                hum = forecast["main"]["humidity"]
                return f"Forecast for {cityname} at {forecast['dt_txt']}: {desc}. Temp {temp}°C, Humidity {hum}%."

        return f"No forecast found for '{target_time}' in {cityname}."

    except Exception as e:
        return f"Weather fetch failed: {e}"
