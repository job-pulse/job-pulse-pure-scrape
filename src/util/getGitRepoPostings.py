import requests
import pandas as pd
from io import StringIO
import json, re, os

if not os.path.exists('getRepoPostings'):
    os.makedirs('getRepoPostings')

def get_content(url):
    response = requests.get(url)
    return response.text

def to_csv(content):
    table_start = content.find('|')
    table_end = content.find('\n\n', table_start)
    table_content = content[table_start:table_end]
    table_lines  = '\n'.join([line.strip() for line in table_content.split('\n') if '🔒' not in line])
    return table_lines

def extract_url(text):
    urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2})|[/])+', str(text))
    return urls[0] if urls else text

def slash_replacer(text):
    return text.replace(r'\/', '/')

def to_json(table_df):
    # table_df = table_df.applymap(extract_url)
    table_json = table_df.to_json(orient='records', lines=True, indent=2)
    table_json = slash_replacer(table_json)

    return table_json

def map_keys(key):
    if any(keyword in key for keyword in ["Company", "Name", "Firm"]):
        return "company"
    elif any(keyword in key for keyword in ["Roles", "Application", "Link", "Title"]):
        return "link"
    elif any(keyword in key for keyword in ["Added On", "Date Posted"]) or "date" in key.lower():
        return "date"
    else:
        return None

def to_conform_json(data):
    dict_strings = data.strip().split('\n\n')
    # Parse each dictionary string and append to the result list
    lines = [json.loads(dict_string) for dict_string in dict_strings]
    transformed_data = []
    for record in lines:
        new_record = {}
        for key, value in record.items():

            new_key = map_keys(key)
            if new_key:
                new_record[new_key] = value
        transformed_data.append(new_record)
    return transformed_data

def to_clean_json_values(data, country):
    transformed_data = []
    for record in data:

        new_record = {
            "title" : "Software Engineer",
            "description" : "",
            "location": country,
            "category": "Software Engineer",
            "title_correct_by_gpt": True,
            "yoe" : 0
            }
        for key, value in record.items():
            if key == "company":

                match = re.search(r'\[([^]]+)\]', value)

                new_record[key.lower()] = match.group(1) if match else value
            elif key == "link":
                new_record["link"] = extract_url(value)
            else:
                new_record[key.lower()] = value.strip()
        transformed_data.append(new_record)
    return transformed_data

def get_table_as_json(url, country):
    content = get_content(url)
    table_content = to_csv(content)
    table_df = pd.read_csv(StringIO(table_content), delimiter='|', skipinitialspace=True, on_bad_lines='skip')
    table_json = to_json(table_df)
    conform_json = to_conform_json(table_json)
    cleaned_json_value = to_clean_json_values(conform_json, country)

    return json.dumps(cleaned_json_value, indent=4, ensure_ascii=False)

def save_json_to_file(json_data, file_name):
    with open(file_name, 'w') as f:
        f.write(str(json_data))

def fetch_and_save_data(urls, output_filename, country):
    all_json_data = []

    for _, url in enumerate(urls):
        table_json = json.loads(get_table_as_json(url, country))
        all_json_data.extend(table_json)  # Extend the list with data from the current URL

    result = []
    for data in all_json_data:
        if not(any(character.isalpha() for character in data['company'] )):
            print(data)
        else:
            result.append(data)

    # Save all_json_data to the file
    with open('getRepoPostings/' +output_filename, 'w') as f:
        json.dump(result, f, indent=2)
    print(f'Saved combined JSON data to {output_filename}')
    return result