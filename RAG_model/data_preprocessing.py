import re
import json
from bs4 import BeautifulSoup

input_file_path = "../MLModelTraining/covenants.json"

with open(input_file_path, 'r') as file:
    data = json.load(file)

cleaned_data = []

for document in data:
    html_content = document['data']['html']
    soup = BeautifulSoup(html_content, 'html.parser')
    full_text = soup.get_text()

    cleaned_text = re.sub(r'\s+', ' ', full_text).strip()

    cleaned_text = re.sub(r'[^\w\s,.!?\'"]', '', cleaned_text)

    cleaned_data.append(cleaned_text)

    break

with open("cleaned_data.txt", "w", encoding='utf-8') as file:
    for item in cleaned_data:
        file.write(item + '\n')

print("Data has been written to cleaned_data.txt")
