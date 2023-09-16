import re

def extract_url(text):
    # get the link of the name 
    urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2})|[/])+', str(text))
    return urls[0] if urls else text

def slash_replacer(text):
    return text.replace(r'\/', '/')


def get_text_display(value):
    # get the displayed name instead of the link itself
    return re.search(r'\[([^]]+)\]', value)

def remove_special_chars(extracted_title):
    cleaned_title = re.sub(r'[^\w\s-]', '', extracted_title.replace("🛂", '').replace('\u2013', '-'))
    return cleaned_title