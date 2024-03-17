from pydantic import BaseModel, root_validator

class Price(BaseModel):
    price: dict

class Item(BaseModel):
    brand: str
    brandId: int
    id: int
    name: str
    feedbacks: int
    reviewRating: float
    sizes: list[Price]
    price: float = 0
    supplier: str
    supplierId: int
    supplierRating: float 
    volume: int 

    @root_validator(pre=True)
    def convert_price(cls, values):
        sale_price = values.get('sizes')[0].get('price', {}).get('product')
        if sale_price is not None:
            values['price'] = sale_price / 100
        return values
    

class Items(BaseModel):
    products: list[Item]


