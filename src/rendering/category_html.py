from src.classes.category import Category
from src.rendering.product_html import HTMLProduct

class HTMLCategory(Category):
    def __init__(self, name, url, products):
        html_products = [
            HTMLProduct(p.ref, p.name, p.url, p.tech, p.safety, p.image)
            for p in products
        ]
        super().__init__(name, url, html_products)

    def to_html(self):
        """html = f""
        <style>
            .category {{
            border: 2px solid #00b894;
            border-radius: 1.5em;
            padding: 32px 28px 24px 28px;
            margin: 32px 0;
            background: linear-gradient(135deg, #e0f7fa 0%, #f9fbe7 100%);
            box-shadow: 0 6px 24px rgba(0,0,0,0.08);
            transition: box-shadow 0.3s;
            }}
            .category:hover {{
            box-shadow: 0 12px 32px rgba(0,0,0,0.15);
            }}
            .category h2 {{
            color: #222;
            margin-bottom: 8px;
            font-size: 2.2em;
            letter-spacing: 1px;
            font-family: 'Segoe UI', Arial, sans-serif;
            }}
            .category a {{
            display: inline-block;
            margin-bottom: 22px;
            color: #00b894;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
            border-bottom: 2px solid #00b89433;
            transition: color 0.2s, border-bottom 0.2s;
            }}
            .category a:hover {{
            color: #0984e3;
            border-bottom: 2px solid #0984e3;
            }}
            .category-products {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 28px;
            margin-top: 10px;
            }}
        </style>"""
        html = f"""
        <div class="category">
            <h2>{self.name}</h2>
            <a href="{self.url}" target="_blank" rel="noopener">Visit category page &rarr;</a>
            <div class="category-products">
        """
        for product in self.products:
            html += product.to_html()
        html += """
            </div>
        </div>
        """
        return html
        