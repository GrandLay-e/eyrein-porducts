#for local testing, uncomment the following lines
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify
from my_api.config import USED_PRODUCTS_REF, MY_KEY
from src.CONST import JSON_FILE, CSS_FILE
from src.functions import json_to_object,format_all_data

from src.rendering.category_html import *

app = Flask(__name__)
# if not __name__ == "__main__":
#     JSON_FILE = "data/Products.json"

with open(CSS_FILE, 'r', encoding='utf-8') as f:
    css_content = f.read()

all_products = json_to_object(JSON_FILE)
formatted_products = format_all_data(all_products)

# Get all products
@app.route('/products/format=<string:format>/', methods=['GET'])
def get_products(format):
    if format == "json":
        return jsonify(formatted_products)
    elif format == "html":
        html_content = f"""<style>{css_content}</style>
        <h1>All Products</h1>
        <p>Here is the list of all products available.</p>"""
        for category in all_products:
            html_category = HTMLCategory(category.name , category.url, category.products)
            # html_category = HTMLCategory(category)
            html_content += html_category.to_html()
        return html_content
    else:
        return jsonify({"error": "Format not supported"}), 400

# Get a single product identified with REF
@app.route('/products/<path:REF>/format=<string:format>/', methods=['GET'])
def get_product_by_ref(REF, format, dictionnary_return=False):
    product = next(
        (product for category in formatted_products for product in category['Products'] if product.get('REF') == REF.upper()),
        None
    )
    if product:
        if dictionnary_return:
            return product
        if format == "json":
            return jsonify(product)
        elif format == "html":
            html_product = HTMLProduct(product['REF'], product['Name'], product['Url'], product['Tech Sheet'], product['Safety Sheet'])
            return f"<style> {css_content}</style>" + html_product.to_html()
        else:
            return jsonify({"error": "Format not supported"}), 400
    else:
        if dictionnary_return:
            return {"Error": "Product Not Found"}
    return jsonify({"error": "Product Not Found"}), 404

# Get only products that my company uses
@app.route('/products/myproducts/key=<string:key>/format=<string:format>/', methods=['GET'])
def get_my_products_by_key(key, format):
    if key == MY_KEY:
        my_products = {ref: get_product_by_ref(ref, format, True) for ref in USED_PRODUCTS_REF}
        if format == "json":
            return jsonify(my_products), 200 
        elif format == "html":
            html_content = f"""
            <style> {css_content}</style>
            <h1>My Products</h1>
            <p>These are the products that my company uses.</p>
            <div class="products-list">
            """
            for ref, product in my_products.items():
                if "REF" in product.keys() :  # Ensure product is not None
                    html_product = HTMLProduct(
                        product.get('REF'),
                        product.get('Name'),
                        product.get('Url'),
                        product.get('Tech Sheet'),
                        product.get('Safety Sheet'),
                        product.get('Image')
                    )
                else:
                    html_product = HTMLProduct(ref, "Unknown Product", "Not Found", "Not Found", "Not Found", "Not Found")
                html_content += html_product.to_html()
            return html_content + "</div>", 200
        else:
            return jsonify({"error": "Format not supported"}), 400
    return jsonify({"Error": "Unauthorized!"}), 401


if __name__ == '__main__':
    app.run(debug=True)
