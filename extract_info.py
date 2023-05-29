# extract_info1.py
import re

state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

def extract_info(text):
    lines = text.split("\n")
    pattern_area = r"^(\d+)\s+([\w\s]+\s+(" + '|'.join(state_list) + "))"  # pattern to accommodate all states
    pattern_item = r"^(\d+)\s+(\d+)\s+(.*?)\s+(\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4})\s+(\d+)"
    pattern_quantity = r"(\d{1,3},\d{3}\.\d{3})"
    pattern_stop = r"^(\d+)\s+LOT:"

    info = []
    current_area = None
    item = {}

    for line in lines:
        stop_match = re.match(pattern_stop, line)
        if stop_match:
            break

        area_match = re.match(pattern_area, line)
        if area_match:
            current_area = area_match.group(2).strip()
            continue
        
        item_match = re.match(pattern_item, line)
        if item_match:
            item = {}
            item['Item Number'] = item_match.group(1)
            item['Material'] = item_match.group(2)
            item['Description'] = item_match.group(3).strip()
            item['Required by'] = item_match.group(4)
            item['ZipCode'] = item_match.group(5)
            item['Area'] = current_area
            continue

        quantity_match = re.match(pattern_quantity, line)
        if quantity_match and item:  
            item['Quantity'] = quantity_match.group(1).replace(",", "")
            info.append(item)  
            item = {}  

    if item:  
        info.append(item)

    return info
