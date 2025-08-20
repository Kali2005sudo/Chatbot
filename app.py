from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from bot.utils import add_placeholder
from bot import memory
from bot.nlp import reply
from bot.config import TYPING_DELAY
from bot.voice import listen_once, speak

M = memory.load()


class ChatUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CodeAlphaBot")
        self.geometry("780x560")
        self.minsize(720, 520)

        # Styles
        self.configure(bg="#0f172a")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", padding=8)
        style.configure("TEntry", padding=6)

        # Header
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", padx=12, pady=10)
        tk.Label(
            header,
            text="🤖 CodeAlphaBot",
            fg="#e2e8f0",
            bg="#0f172a",
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left")
        self.status = tk.Label(header, text="Ready", fg="#94a3b8", bg="#0f172a")
        self.status.pack(side="right")

        # Chat area
        body = tk.Frame(self, bg="#0f172a")
        body.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        self.text = tk.Text(
            body,
            wrap="word",
            state="disabled",
            bg="#111827",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            relief="flat",
            padx=12,
            pady=12,
        )
        self.text.pack(fill="both", expand=True, side="top")
        self.text.tag_configure("bot", foreground="#a7f3d0")
        self.text.tag_configure("user", foreground="#93c5fd")

        # Input row
        row = tk.Frame(body, bg="#0f172a")
        row.pack(fill="x", side="bottom", pady=(8, 0))

        self.entry = tk.Entry(row, bg="#1e293b", relief="flat", insertbackground="white")
        self.entry.pack(side="left", fill="x", expand=True)
        add_placeholder(self.entry, "Type a message or ask me anything...")

        self.entry.bind("<Return>", self.on_send)
        ttk.Button(row, text="Send", command=self.on_send).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(row, text="Help", command=self.quick_help).pack(side="left", padx=6)
        ttk.Button(row, text="Reminders", command=self.quick_reminders).pack(
            side="left"
        )
        ttk.Button(row, text="🎤", command=self.on_mic).pack(side="left", padx=6)

        # Welcome
        self._append(
            "bot",
            "Hello! Type 'help' or try: weather in Lahore, remind me in 10 mins tea, translate to ur Hello.",
        )
        self.entry.focus_set()

    def _append(self, who: str, msg: str):
        self.text.configure(state="normal")
        self.text.insert("end", f"{'You' if who=='user' else 'Bot'}: {msg}\n", who)
        self.text.configure(state="disabled")
        self.text.see("end")

    def on_send(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, "end")
        self._append("user", msg)

        try:
            # ✅ Agar user "/search ..." likhe to PDF me search karo
            if msg.startswith("/search "):
                from bot.pdf_handler import search_pdf
                query = msg.replace("/search ", "").strip()
                out = search_pdf(query)

            else:
                # Normal chatbot reply
                out = reply(M, msg)

            self._append("bot", out)
            speak(M, out)  # voice TTS if enabled
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        finally:
            memory.save(M)

    def quick_help(self):
        self._append(
            "bot",
            "Try: 'weather in Karachi', 'remind me next Monday 7pm groceries', 'translate to ur Thank you', 'table 7 up to 12'.",
        )

    def quick_reminders(self):
        from bot.reminders import list_reminders

        self._append("bot", list_reminders(M))
    
    # -------------------
    # Mic listener method
    # -------------------
    def on_mic(self):
        self._append("bot", "🎤 Listening...")
        text, error = listen_once()
        if error:
            self._append("bot", f"Error: {error}")
        else:
            self.entry.delete(0, "end")
            self.entry.insert(0, text)
            self.on_send()


if __name__ == "__main__":
    ChatUI().mainloop()
