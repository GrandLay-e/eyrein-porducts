from flask import Flask, jsonify
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_api.config import USED_PRODUCTS_REF, MY_KEY
from src.CONST import JSON_FILE
from src.functions import json_to_object

# from src.rendering.product_html import HTMLProduct
from src.rendering.category_html import *

app = Flask(__name__)
if not __name__ == "__main__":
    JSON_FILE = "data/Products.json"

print("NAME FILE",__name__)
# try:
#     with open(JSON_FILE, 'r', encoding='utf-8') as f:
#         all_products = json.load(f)
#         print("Bien Pris ! ")
# except Exception as e:
#     print("Pas récupèré ! ", e)
#     all_products = []

all_products = json_to_object(JSON_FILE)

# Get all products
@app.route('/products/', methods=['GET'])
def get_products():
    return jsonify(all_products)

# Get a single product identified with REF
@app.route('/products/<path:REF>/')
def get_product(REF, dictionnary_return = False):
    product = next(
        (product for category in all_products for product in category['Products'] if product.get('REF') == REF.upper()),
        None
    )
    if product:
        if dictionnary_return:
            return product
        return jsonify(product)
    return {"Error" : "Product not Found"} if dictionnary_return else (jsonify({"error": "Not Found"}), 404)

# Get only products that my company uses
@app.route('/products/myproducts/key=<string:key>/', methods=['GET'])
def get_my_products(key):
    if key == MY_KEY:
        my_products = {ref:get_product(ref, True) for ref in USED_PRODUCTS_REF}
        return jsonify(my_products), 200 
    return jsonify({"Error": "Unauthorized!"}), 401 

if __name__ == '__main__':
    app.run(debug=True)
