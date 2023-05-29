# main.py
import os
import pandas as pd
from pdf_to_text import pdf_to_text
from extract_info import extract_info

def main():
    pdf_folder_path = 'pdfs'
    excel_folder_path = 'excels'

    for pdf_file in os.listdir(pdf_folder_path):
        if pdf_file.endswith('.pdf'):
            pdf_file_path = os.path.join(pdf_folder_path, pdf_file)
            print(f"Processing {pdf_file}...")
            text = pdf_to_text(pdf_file_path)
            if text:
                print(f"Extracting information from {pdf_file}...")
                info = extract_info(text)
                if info:
                    print("Information extracted.")
                    excel_file_path = os.path.join(excel_folder_path, f'{os.path.splitext(pdf_file)[0]}.xlsx')
                    df = pd.DataFrame(info)
                    df.to_excel(excel_file_path, index=False)
                    print(f"Excel file created: {excel_file_path}")
                else:
                    print("No information extracted from the text.")
            else:
                print(f"Failed to extract text from {pdf_file}.")

if __name__ == '__main__':
    main()
