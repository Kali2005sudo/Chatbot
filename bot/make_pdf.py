import os
from reportlab.pdfgen import canvas


def make_pdf():
    # always save inside bot/ folder
    base_dir = os.path.dirname(__file__)  # current folder (bot/)
    pdf_path = os.path.join(base_dir, "manual.pdf")

    c = canvas.Canvas(pdf_path)

    # Page 1: Introduction
    c.drawString(100, 750, "Welcome to CodeAlphaBot Manual")
    c.drawString(
        100,
        720,
        "This bot can answer your questions and also search inside this manual.",
    )
    c.drawString(100, 690, "Technologies used: Python, Tkinter, ReportLab, PyPDF2.")
    c.showPage()

    # Page 2: Installation
    c.drawString(100, 750, "Installation Steps")
    c.drawString(100, 720, "1. Install Python 3.10 or higher")
    c.drawString(100, 690, "2. Clone the project repository")
    c.drawString(100, 660, "3. Install dependencies: pip install -r requirements.txt")
    c.drawString(100, 630, "4. Run the bot: python app.py")
    c.showPage()

    # Page 3: Usage
    c.drawString(100, 750, "Usage Instructions")
    c.drawString(100, 720, "You can chat normally by typing your questions.")
    c.drawString(100, 690, "For searching manual content, type /search keyword")
    c.drawString(100, 660, "Example: /search installation")
    c.drawString(100, 630, "Example: /search python")
    c.showPage()

    # Page 4: Commands Reference
    c.drawString(100, 750, "Commands Reference")
    c.drawString(100, 720, "/search <word> → Search inside manual.pdf")
    c.drawString(100, 690, "/help → Show available commands")
    c.drawString(100, 660, "/voice on → Enable voice replies")
    c.drawString(100, 630, "/voice off → Disable voice replies")
    c.showPage()

    # Page 5: Troubleshooting
    c.drawString(100, 750, "Troubleshooting Guide")
    c.drawString(100, 720, "If Python is not found, check your PATH variable.")
    c.drawString(100, 690, "If dependencies fail, delete .venv and reinstall.")
    c.drawString(100, 660, "If chatbot does not respond, check internet connection.")
    c.drawString(
        100, 630, "If PDF search fails, make sure the file exists in the bot/ folder."
    )
    c.showPage()

    c.save()

    # ✅ confirmation message
    print(f"✅ manual.pdf created at: {pdf_path}")


make_pdf()
