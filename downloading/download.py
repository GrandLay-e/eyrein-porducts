import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from pathlib import Path
from src.functions import json_to_object, logging
from src.CONST import JSON_FILE
from my_api.config import USED_PRODUCTS_REF
import requests

MAIN_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent/"Downloads ALL"
data = json_to_object(JSON_FILE)

all_used_products = [product for category in data for product in category.products if product.ref in USED_PRODUCTS_REF]

def construct_all_dirs(products, main_dir):
    return [Path(main_dir / f"{p.name}") for p in products]

all_dirs = construct_all_dirs(all_used_products, MAIN_DIR)
def download_pdf(url, dest_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Downloaded {url} to {dest_path}")
    except Exception as e:
        logging.error(f"Failed to download {url}: {e}")


def create_dirs(dirs):
    for dir in dirs:

        os.makedirs(dir, exist_ok=True)

if __name__ == "__main__":
    create_dirs(all_dirs)
    for product, dir in zip(all_used_products, all_dirs):
        if hasattr(product, 'tech') and product.tech:
            download_pdf(product.tech , dir/f"fiche_technique_{product.name}.pdf")
        if hasattr(product, 'safety') and product.safety:
            download_pdf(product.safety, dir/f"fiche_de_sécurité_{product.name}.pdf")
