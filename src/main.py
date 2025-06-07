from functions import *
from pprint import pprint
import logging

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#
def get_data_from_web():
    soup = get_page(SHOP_URL)
    categories = {category['title']: urljoin(SHOP_URL, category['href']) for category in get_element(soup, BLOCK)}
    DATA = []
    for name, url in categories.items():
        category_data = {
            "Category name": name,
            "Category URL": url,
            "Products": []
        }
        seen_products = set()
        all_pages = get_all_pages(url)
        for page in all_pages:
            soup_products = get_page(page)
            product_blocks = get_element(soup_products, BLOCK)
            for block in product_blocks:
                product_url = urljoin(SHOP_URL, block['href'])
                if product_url in seen_products:
                    continue  # Skip duplicate product
                seen_products.add(product_url)
                product_page = get_page(product_url)
                product_name = get_element(product_page, TITLE)[0].get_text().strip()
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
                logging.info(f"Product name : {product_name}")
        DATA.append(category_data)
    return DATA

DATA = get_data_from_web()
save_json(JSON_FILE, DATA)