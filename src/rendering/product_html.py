from src.classes.product import Product

class HTMLProduct(Product):
    
    def __init__(self, ref, name, url, tech, safety, image):
        super().__init__(ref, name, url, tech, safety, image)

    def to_html(self):
        
        """base_style = ""
        <style>
        .product {
            border: 1px solid #222831;
            border-radius: 14px;
            padding: 22px;
            margin: 24px 0;
            background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%);
            box-shadow: 0 4px 24px rgba(34, 40, 49, 0.10);
            max-width: 540px;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            transition: box-shadow 0.3s;
        }
        .product:hover {
            box-shadow: 0 8px 32px rgba(41, 128, 185, 0.18);
        }
        .product h3 {
            margin-top: 0;
            color: #222831;
            font-size: 1.6em;
            letter-spacing: 1px;
        }
        .product .infos {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 18px;
        }
        .product .image img {
            max-width: 120px;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(41, 128, 185, 0.10);
            background: #fff;
        }
        .product .texts {
            flex: 1;
        }
        .product .texts p {
            margin: 10px 0;
            font-size: 1.08em;
            color: #393e46;
        }
        .product .texts a {
            color: #2980b9;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        .product .texts a:hover {
            color: #222831;
            text-decoration: underline;
        }
        .product.unknown {
            border: 2px dashed #e74c3c;
            background: linear-gradient(135deg, #fff0f0 0%, #ffeaea 100%);
            box-shadow: 0 2px 12px rgba(231, 76, 60, 0.10);
        }
        .product.unknown h3 {
            color: #e74c3c;
        }
        .product.unknown .texts p {
            color: #c0392b;
        }
        </style>
        """

        if (
            self.name == "Unknown Product"
            and self.url == "Not Found"
            and self.tech == "Not Found"
            and self.safety == "Not Found"
        ):
            html = f"""
            <div class="product unknown">
            <h3>Unknown Product</h3>
            <div class="infos">
                <div class="texts">
                <p><strong>{self.ref}</strong></p>
                <p>Product page: Not found</p>
                <p>Technical sheet: Not found</p>
                <p>Safety sheet: Not found</p>
                </div>
            </div>
            </div>
            """
        else:
            html = f"""
            <div class="product">
            <h3>{self.name}</h3>
            <div class="infos">
                <div class="image">
                <img src="{self.image}" alt="{self.name}">
                </div>
                <div class="texts">
                <p><strong>{self.ref}</strong></p>
                <a href="{self.url}" target="_blank" rel="noopener">Product page</a></p>
                <a href="{self.tech}" target="_blank" rel="noopener">Technical sheet</a></p>"""
            if self.safety != "Not Found":
                html += f"""
                <a href="{self.safety}" target="_blank" rel="noopener">Safety sheet</a></p>"""
            html += """
                </div>
            </div>
            </div>
            """
        return html