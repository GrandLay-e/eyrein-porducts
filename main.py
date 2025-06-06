from urllib.parse import urljoin
from CONST import *
from functions import *
from pprint import pprint
import time

soup = get_page(SHOP_URL)
categories = {category['title'] : urljoin(SHOP_URL , category['href']) for category in get_element(soup, BLOCK)}
DATA = []
for name, url in categories.items():
    category_data = {
        "Category name": name,
        "Category URL": url,
        "Products": []
    }
    all_pages = get_all_pages(url)
    for page in all_pages:
        soup_products = get_page(page)
        product_blocks = get_element(soup_products, BLOCK)
        for block in product_blocks:
            product_url = urljoin(SHOP_URL, block['href'])
            product_name = block.select('h2')[0].get_text()
            product_page = get_page(product_url)
            product_ref = get_element(product_page, REF)[1].get_text()
            product_sheets = get_element(product_page, SHEETS)
            tech_sheet = product_sheets[0]['href'] if len(product_sheets) > 0 else "Not Found"
            safety_sheet = product_sheets[1]['href'] if len(product_sheets) > 1 and product_sheets[1].get('href') else "Not Found"
            category_data["Products"].append({
                "Product Name": product_name,
                "Product Url": product_url,
                "REF": product_ref,
                "Technical Sheet": tech_sheet,
                "Safety Sheet": safety_sheet
            })
    DATA.append(category_data)
save_json(JSON_FILE, DATA)