import requests
from bs4 import BeautifulSoup

import json
import logging
from urllib.parse import urljoin

from CONST import *

def get_page(session,url, get_url = False):
        response = session.get(url)
        if get_url == True:
            return response.url
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        logging.debug("Problème requests")
        return None

def get_element(soup, selector):
    try:
        return soup.select(selector)
    except Exception as e:
        logging.error(f"ERROR : {e}")

def get_all_pages(session, url):
    soup = get_page(session, url)
    first = get_page(session, url, True)
    number_of_pages = int([link['href'].split("=")[1] for link in soup.select('.pager a') if link.get_text() == "dernier"][0])
    pages = [urljoin(first +"/", f"?page={i}") for i in range(1,number_of_pages+1)]
    return pages

def save_json(file, new_data):
    try:
        with open(file,"r", encoding='utf-8') as f:
            data = json.load(f)
            data.extend(new_data)
    except FileNotFoundError as e:
        logging.error(f"Error while reading json file : {file}\n {e}")
        data = new_data
    try:
        with open(file,"w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error while writing in json file {file}\n {e}")
