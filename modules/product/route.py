from fastapi import APIRouter,Depends
from database.database import get_db
from sqlalchemy.orm import Session
from modules.product.crud import add_product,place_order,get_top_products
from modules.product.schema import AddSchema,OrderSchema


router=APIRouter()

@router.post('/add-product')
def create_product(schema:AddSchema,db:Session=Depends(get_db)):
    res=add_product(schema,db)
    return res

@router.post("/place-order")
def create_order(schema: OrderSchema, db: Session = Depends(get_db)):
    res = place_order(schema, db)
    return res

@router.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    res = get_top_products(db)
    return res
