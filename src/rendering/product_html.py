from src.classes.product import Product

class HTMLProduct(Product):
    
    def __init__(self, ref, name, url, tech_sheet, safety_sheet):
        super().__init__(ref, name, url, tech_sheet, safety_sheet)

    def to_html(self):
        html = f"""
        <link rel="stylesheet" type="text/css" href="style.css">
        <div class="product">
            <h3>{self.name}</h3>
            <div class="infos">
            <p>Reference: {self.ref}</p>
            <p><a href="{self.url}">Product page</a></p>
            <p><a href="{self.tech_sheet}">Technical sheet</a></p>
            <p><a href="{self.safety_sheet}">Safety sheet</a></p>
            </div>
        </div>
        """
        return html