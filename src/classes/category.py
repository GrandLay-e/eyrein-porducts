from .product import Product

class Category:
    def __init__(self,name, url, products : list[Product]):
        self.name =  name
        self.url = url
        self.products = products

    def format_category(self):
        return{
            "Category Name" : self.name,
            "Category URL" : self.url,
            "Products" : [product.format_product() for product in self.products]
        }
    
    