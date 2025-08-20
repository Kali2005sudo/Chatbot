# bot/pdf_handler.py
import os
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Read PDF and return text content as string.
    """
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def search_pdf(query, pdf_path=None):
    """
    Search query in given PDF and return matching snippet.
    Default = manual.pdf
    """
    base_dir = os.path.dirname(__file__)
    if not pdf_path:  # agar user ne path nahi diya
        pdf_path = os.path.join(base_dir, "manual.pdf")
    else:
        pdf_path = os.path.join(base_dir, pdf_path)

    pdf_text = extract_text_from_pdf(pdf_path)

    # Simple keyword search
    query = query.lower()
    lines = pdf_text.splitlines()
    matches = [line for line in lines if query in line.lower()]

    if not matches:
        return "❌ No information found in manual."

    return "\n".join(matches[:3])
