from bot.pdf_handler import search_pdf


def process_user_message(message):
    """
    Decide bot ka reply.
    """
    if message.startswith("/search "):  # agar /search command use kare
        query = message.replace("/search ", "").strip()
        return search_pdf(query)

    # fallback reply
    return f"🤖 I received: {message}"
