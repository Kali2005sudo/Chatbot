from __future__ import annotations

# optional deps; ignore unresolved in editor
try:
    import speech_recognition as sr  # type: ignore[import-not-found]
except Exception:
    sr = None

try:
    import pyttsx3  # type: ignore[import-not-found]

    TTS = pyttsx3.init()
except Exception:
    pyttsx3 = None
    TTS = None


def toggle_voice(M, on: bool | None = None):
    M["voice_on"] = (not M.get("voice_on")) if on is None else bool(on)
    return f"Voice mode {'enabled' if M['voice_on'] else 'disabled'}."


def listen_once(timeout=5, phrase_time_limit=7):
    if not sr:
        return (
            None,
            "Speech recognition not available. Install SpeechRecognition & pyaudio.",
        )
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic, duration=0.5)
        try:
            audio = rec.listen(
                mic, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
            txt = rec.recognize_google(audio)
            return txt, None
        except sr.WaitTimeoutError:
            return None, "Listening timed out."
        except Exception as e:
            return None, f"Speech recognition error: {e}"


def speak(M, text: str):
    if M.get("voice_on") and TTS:
        try:
            TTS.say(text)
            TTS.runAndWait()
        except Exception:
            pass
