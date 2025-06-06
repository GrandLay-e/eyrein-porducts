import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from CONST import *

def get_page(url, get_url = False):
    with requests.Session() as Session:
        response = Session.get(url)
        print(response.url)
        if get_url == True:
            return response.url
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None

def get_element(soup, selector):
    return soup.select(selector)

def get_all_pages(url):
    soup = get_page(url)
    first = get_page(url, True)
    number_of_pages = int([link['href'].split("=")[1] for link in soup.select('.pager a') if link.get_text() == "dernier"][0])
    pages = [urljoin(first +"/", f"?page={i}") for i in range(1,number_of_pages+1)]
    return pages

def save_json(file, new_data):
    try:
        with open(file,"r", encoding='utf-8') as f:
            data = json.load(f)
            print("SUCCES READING")
            data.extend(new_data)
    except Exception as e:
        print(f"Error while reading json file : {file}\n {e}")
        data = new_data
    try:
        with open(file,"w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            print("SUCCESS WRITING")
    except Exception as e:
        print(f"Error while writing in json file {file}\n {e}")

if __name__ == '__main__':
    save_json(JSON_FILE, {})