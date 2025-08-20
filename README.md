# CodeAlphaBot
🤖
**CodeAlphaBot** is an advanced Python chatbot featuring multi-modal interaction: text chat,
voice input/output, PDF search, weather updates, translation, math operations, fun facts,
reminders, and more.
---
##
🚀 Features
1. **Text Chat** – Intelligent chatbot capable of natural language conversation.
2. **Voice Chat** – Microphone input and Text-to-Speech responses.
3. **PDF Search** – Query PDF manuals using `/search <query>`.
4. **Weather Forecast** – Current and forecast weather using OpenWeatherMap API.
5. **Translation** – Translate text into multiple languages.
6. **Math & Conversion** – Quick calculations and unit conversions.
7. **Fun & Trivia** – Jokes, facts, and compliments.
8. **Reminders** – Set and list reminders.
9. **Graphical Interface** – Tkinter-based GUI with chat area and input box.
---
##
🗂 Project Structure
chat_bot/
│── app.py # Entry point (GUI)
│── requirements.txt # Python dependencies
│── .venv/ # Virtual environment
│
├── bot/
│ ├── init.py
│ ├── config.py # API keys and constants
│ ├── memory.py # Save/load user memory
│ ├── utils.py # Helpers (text cleaning, fuzzy search)
│ ├── nlp.py # Chatbot NLP & replies
│ ├── reminders.py # Reminders feature
│ ├── mathx.py # Math & conversion
│ ├── fun.py # Jokes, facts, compliments
│ ├── weather.py # Weather feature
│ ├── voice.py # Speech recognition + TTS
│ ├── translator.py # Translation feature
│ └── pdf_handler.py # PDF search handler
│
└── data/├── bot_memory.json # Persistent memory
├── jokes.json
├── facts.json
├── synonyms.json
└── compliments.json
---
## ⚙ Installation
1. Clone the repository:
```bash
git clone <your-repo-url>
cd chat_bot
Required Python libraries:
blinker==1.9.0
certifi==2025.8.3
chardet==3.0.4
charset-normalizer==3.4.3
click==8.2.1
Flask==3.1.2
fuzzywuzzy==0.18.0
googletrans==4.0.0rc1
h11==0.9.0
h2==3.2.0
hpack==3.0.0
hstspreload==2025.1.1
httpcore==0.9.1
httpx==0.13.3
hyperframe==5.2.0
idna==2.10
itsdangerous==2.2.0
Jinja2==3.1.6
joblib==1.5.1
Levenshtein==0.27.1
MarkupSafe==3.0.2nltk==3.9.1
PyAudio==0.2.14
pyspellchecker==0.8.3
python-dotenv==1.1.1
python-Levenshtein==0.27.1
pyttsx3==2.99
RapidFuzz==3.13.0
regex==2025.7.34
requests==2.32.5
rfc3986==1.5.0
schedule==1.2.2
sniffio==1.3.1
SpeechRecognition==3.14.3
tqdm==4.67.1
typing_extensions==4.14.1
urllib3==2.5.0
Werkzeug==3.1.3
