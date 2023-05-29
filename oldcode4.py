import pdfplumber
import pandas as pd
import re
from collections import namedtuple

def extract_data_from_pdf(file):
    Item = namedtuple('Item', 'Item_Number Material Required_by ZipCode Quantity')

    data = []
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                if line.startswith(('Item', 'If')):
                    continue

                # match item number and material
                match = re.search(r'(\d{4,5})\s([A-Za-z].*?)\s(\d+,\d+\.\d+)', line)
                if match:
                    item_number, material, quantity = match.groups()
                    line = line.replace(item_number, '').replace(material, '').replace(quantity, '')

                # match required by and zipcode
                match = re.search(r'(\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4})\s(\d{5})', line)
                if match:
                    required_by, zipcode = match.groups()
                    line = line.replace(required_by, '').replace(zipcode, '')

                    data.append(Item(item_number, material, required_by, zipcode, quantity))

    return data

def convert_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    data = extract_data_from_pdf('pdfs/sample1.pdf')  # replace 'file.pdf' with your file path
    convert_to_excel(data, 'excels/output.xlsx')  # replace 'output.xlsx' with your preferred filename

if __name__ == "__main__":
    main()
