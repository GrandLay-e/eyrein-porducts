import json

class Product:
    def __init__(self, ref, name, url, tech_sheet ,safety_sheet):
        self.ref = ref
        self.name = name
        self.url = url
        self.tech = tech_sheet
        self.safety = safety_sheet

    def format_product(self) -> dict[str:str]:
        return{
            "REF" : self.ref,
            "Name" : self.name,
            "Url" : self.url,
            "Tech Sheet" : self.tech,
            "Safety Sheet" : self.safety
        }

    def save_product(self):
        pass