from pydantic import BaseModel

class AddSchema(BaseModel):
    name:str
    price:float
    stock_qty:int

class OrderSchema(BaseModel):
    product_id: int
    quantity: int    