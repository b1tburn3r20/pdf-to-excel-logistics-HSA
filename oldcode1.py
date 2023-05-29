import os
import re
import pdfplumber
import pandas as pd

def extract_text_from_pdf(pdf_path):
    print(f"Opening the PDF file: {pdf_path}")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            print(f"Extracting text from page {i+1}/{total_pages}")
            text += f"\nPage {i+1}\n{page.extract_text()}\n"
    print("Text extraction completed.")
    return text


# define all possible states abbreviations in USA
state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

def extract_info(text):
    lines = text.split("\n")
    pattern_line1 = r"^(\d+)\s+(\d+)\s+(.*?)\s+(\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4})\s+(\d+)"
    pattern_line2 = r"(\d{1,3},\d{3}\.\d{3})"
    pattern_area = r"^(\d+)\s+([\w\s]+\s+(" + '|'.join(state_list) + "))"  # pattern to accommodate all states
    pattern_lot = r"^(\d+)\s+LOT:\s+(\d+)\s+((?:[\w\s]+/)+)"  # pattern to accommodate LOT lines

    info = []
    current_area = None
    current_lot = None
    current_lot_number = None
    item = {}

    for line in lines:
        lot_match = re.match(pattern_lot, line)
        if lot_match:
            current_lot = [x.strip() for x in lot_match.group(3).split('/') if x.strip()]
            current_lot_number = lot_match.group(2)
            continue

        area_match = re.match(pattern_area, line)
        if area_match:
            current_area = area_match.group(2).strip()
            continue
        
        line1_match = re.match(pattern_line1, line)
        if line1_match:
            item = {}  # Create a new item for each matched line
            item['Item Number'] = line1_match.group(1)
            item['Material'] = line1_match.group(2)
            item['Description'] = line1_match.group(3).strip()
            item['Required by'] = line1_match.group(4)
            item['ZipCode'] = line1_match.group(5)
            item['Area'] = current_area  # Assign the current area to the item
            item['Destinations'] = current_lot  # Assign the current lot to the item as Destinations
            item['Lot Number'] = current_lot_number  # Assign the current_lot_number to the item
            continue

        line2_match = re.match(pattern_line2, line)
        if line2_match and item:  # Only if there is an item already created
            item['Quantity'] = line2_match.group(1).replace(",", "")
            info.append(item)  # Add the completed item to the info list
            item = {}  # Reset the item

    if item:  # If there is any item left
        info.append(item)

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

