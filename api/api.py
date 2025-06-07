from flask import Flask, jsonify, request
import json

from config import USED_PRODUCTS_REF, MY_KEY

JSON_FILE = "../data/Products.json"
app = Flask(__name__)
try:
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        all_products = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    all_products = [] 

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
