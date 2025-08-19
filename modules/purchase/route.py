from fastapi import APIRouter,Depends, Query,UploadFile,File,HTTPException
from database.database import get_db
from sqlalchemy.orm import Session
from modules.purchase.crud import get_purchase_orders,process_and_create_po
from modules.purchase.schema import PurchaseOrderOut
from datetime import date
from typing import Optional


router = APIRouter()

@router.post("/upload_po", response_model=PurchaseOrderOut)
async def upload_po(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return process_and_create_po(file, db)


@router.get("/purchase_order") 
def list_purchase_orders(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return get_purchase_orders(start_date, end_date, db)


