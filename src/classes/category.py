import json
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
            "Products" : self.products
        }
    
    def save_data(self, file, logging):
        try:
            with open(file,"r", encoding='utf-8') as f:
                data = json.load(f)
                data.extend([self.format_category()])
        except Exception as e:
            logging.error(f"Error while reading json file : {file}\n {e}")
            data = [self.format_category()]
        try:
            with open(file,"w", encoding='utf-8') as f:
                json.dump([data], f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error while writing in json file {file}\n {e}")

if __name__ == "__main__":
    product1 = Product("A454K", "Produit Bureau", "bureau.com", "tech.pdf", "safety.pdf")
    product2 = Product("B123X", "Produit Maison", "maison.com", "tech2.pdf", "safety2.pdf")
    product3 = Product("C789Y", "Produit Jardin", "jardin.com", "tech3.pdf", "safety3.pdf")
    product4 = Product("D456Z", "Produit Cuisine", "cuisine.com", "tech4.pdf", "safety4.pdf")
    product5 = Product("E321W", "Produit Garage", "garage.com", "tech5.pdf", "safety5.pdf")
    product6 = Product("F654V", "Produit Salle de Bain", "salledebain.com", "tech6.pdf", "safety6.pdf")
    

    my_category = Category("INNOVER", "INNOVER.COM", [
        product1.format_product(), product2.format_product(), product3.format_product(), product4.format_product(), product5.format_product(), product6.format_product()
    ])

    my_category.save_data('test.json')