import os
import re
import pdfplumber
import pandas as pd

def extract_text_from_pdf(pdf_path, num_pages=5):
    print(f"Opening the PDF file: {pdf_path}")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:num_pages]):
            print(f"Extracting text from page {i+1}")
            text += f"Page {i+1}\n{page.extract_text()}\n"
    print("Text extraction completed.")
    return text


def extract_info(text):
    lines = text.split("\n")
    pattern_line1 = r"^(\d+)\s+(\d+)\s+(.*?)\s+(\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4})\s+(\d+)"
    pattern_line2 = r"(\d{1,3},\d{3}\.\d{2})"
    pattern_area = r"(\d+\s+[\w\s]+\s+AZ)"

    info = []
    area = None  # The area is initially unknown
    for i, line in enumerate(lines):
        match_line1 = re.match(pattern_line1, line)
        match_line2 = re.match(pattern_line2, lines[i+1] if i+1 < len(lines) else "")
        match_area = re.match(pattern_area, line)

        if match_area:
            area = match_area.group(0).strip()  # Update the area
        elif match_line1 and match_line2:
            bid_number = match_line1.group(1)
            item_number = match_line1.group(2)
            description = match_line1.group(3).strip()
            date_range = match_line1.group(4)
            zipcode = match_line1.group(5)
            quantity = match_line2.group(1).replace(",", "")
            unit = 'CS'  # If 'CS' is a fixed value, just assign it directly here.

            info.append({
                'Area': area,
                'Bid Number': bid_number,
                'Item Number': item_number,
                'Description': description,
                'Date Range': date_range,
                'Zipcode': zipcode,
                'Quantity': quantity,
                'Unit': unit
            })

    print("Information extraction completed.")
    return info



def create_excel(info, output_path):
    df = pd.DataFrame(info)
    df.to_excel(output_path, index=False)
    print(f"Excel file created: {output_path}")

def main():
    pdf_folder_path = 'pdfs'
    excel_folder_path = 'excels'

    for pdf_file in os.listdir(pdf_folder_path):
        if pdf_file.endswith('.pdf'):
            pdf_file_path = os.path.join(pdf_folder_path, pdf_file)
            print(f"Processing {pdf_file}...")
            text = extract_text_from_pdf(pdf_file_path)
            if text:
                print(f"Extracting information from {pdf_file}...")
                info = extract_info(text)
                if info:
                    print("Information extracted.")
                    excel_file_path = os.path.join(excel_folder_path, f'{os.path.splitext(pdf_file)[0]}.xlsx')
                    create_excel(info, excel_file_path)
                else:
                    print("No information extracted from the text.")
            else:
                print(f"Failed to extract text from {pdf_file}.")



if __name__ == '__main__':
    main()
