from src.classes.category import Category
from src.rendering.product_html import HTMLProduct

class HTMLCategory(Category):
    def __init__(self, name, url, products):
        html_products = [
            HTMLProduct(p.ref, p.name, p.page, p.tech_sheet, p.safety_sheet)
            for p in products
        ]
        super().__init__(name, url, html_products)

    def to_html(self):
        html =  f"""
        <link rel="stylesheet" type="text/css" href="style.css">
        <div class="category">
            <h2> {self.name} </h2>
            <a href="{self.url}"> Catégory's page </a>
        </div>
        """
        for product in self.products():
            html += product.to_html()

        return html
        