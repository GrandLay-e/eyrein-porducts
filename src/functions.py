#for local testing, uncomment the following lines
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup

from src.rendering.category_html import HTMLCategory
from src.classes.category import Category
from src.classes.product import Product

import json
import logging
from urllib.parse import urljoin

from src.CONST import *

logging.basicConfig(
    # filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    data = json_to_object(file)
    data.extend(new_data)
    try:
        with open(file,"w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error while writing in json file {file}\n {e}")


def get_data_from_web():
    with requests.Session() as session:
        soup = get_page(session, SHOP_URL)
        categories = {category['title']: urljoin(SHOP_URL, category['href']) for category in get_element(soup, BLOCK)}
        DATA = []
        for name, url in categories.items():
            category = Category(name, url, [])
            seen_products = set()
            all_pages = get_all_pages(session, url)
            for page in all_pages:
                i=0
                soup_products = get_page(session,page)
                product_blocks = get_element(soup_products, BLOCK)
                for block in product_blocks:
                    product_url = urljoin(SHOP_URL, block['href'])
                    if product_url in seen_products:
                        continue
                    seen_products.add(product_url)
                    product_page = get_page(session,product_url)
                    product_name = get_element(product_page, TITLE)[0].get_text().strip()
                    product_ref = get_element(product_page, REF)[1].get_text()
                    product_sheets = get_element(product_page, SHEETS)
                    tech_sheet = product_sheets[0]['href'] if len(product_sheets) > 0 else "Not Found"
                    safety_sheet = product_sheets[1]['href'] if len(product_sheets) > 1 and product_sheets[1].get('href') else "Not Found"
                    image = get_element(product_page, IMG_SRC)[0]['src'] if get_element(product_page, IMG_SRC) else "Not Found"
                    product = Product(product_ref, product_name, product_url, tech_sheet, safety_sheet, image)
                    category.products.append(product)
                    logging.info(f"{name} --> {product_name} Image : {"Pas Trouvé" if image == 'Not Found' else "Trouvé"}")
            DATA.append(category.format_category())
    return DATA

def json_to_object(file):
    try:
        with open(file, "r", encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        data = []
        logging.error("Error :", e)
    categories = []
    for cat in data:
        category = Category(
            name=cat.get("Category Name"),
            url=cat.get("Category URL"),
            products=[]
        )
        for prod in cat.get("Products", []):
            product = Product(
                ref=prod.get("REF"),
                name=prod.get("Name"),
                url=prod.get("Url"),
                tech_sheet=prod.get("Tech Sheet"),
                safety_sheet=prod.get("Safety Sheet"),
                image=prod.get("Image", None)
            )
            category.products.append(product)
        categories.append(category)
    return categories

def format_all_data(data):
    formatted_data = []
    for category in data:
        formatted_data.append(category.format_category())
    return formatted_data

if __name__ =='__main__':
    pass