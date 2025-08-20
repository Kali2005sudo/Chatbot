from __future__ import annotations

# optional dep; ignore unresolved in editor
try:
    from googletrans import Translator  # type: ignore[import-not-found]

    _translator = Translator()
except Exception:
    _translator = None


def translate(text: str, dest="ur"):
    if not _translator:
        return "Translate needs 'googletrans'. Try: pip install googletrans==4.0.0-rc1"
    try:
        return _translator.translate(text, dest=dest).text
    except Exception as e:
        return f"Translate failed: {e}"
