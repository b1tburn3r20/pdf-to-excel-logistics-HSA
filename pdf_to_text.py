# pdf_to_text.py
import pdfplumber

def pdf_to_text(pdf_path):
    print(f"Opening the PDF file: {pdf_path}")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            print(f"Extracting text from page {i+1}/{total_pages}")
            text += f"\nPage {i+1}\n{page.extract_text()}\n"
    print("Text extraction completed.")
    return text
