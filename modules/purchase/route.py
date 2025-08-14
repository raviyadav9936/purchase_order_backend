from fastapi import APIRouter,Depends, Query,UploadFile,File,HTTPException
from database.database import get_db
from sqlalchemy.orm import Session
from modules.purchase.crud import create_purchase_order,get_purchase_orders
from modules.purchase.schema import PurchaseOrderCreate,PurchaseOrderOut,PurchaseOrderFilter
from modules.purchase.utils import extract_text_from_pdf, parse_po_details
from datetime import datetime, date
from typing import List, Optional
import os


UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()


@router.post("/upload_po", response_model=PurchaseOrderOut)
async def upload_po(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename
    if not (filename.lower().endswith(".pdf") or filename.lower().endswith((".png", ".jpg", ".jpeg"))):
        raise HTTPException(status_code=400, detail="Only PDF / PNG / JPG files supported")

    saved_path = os.path.join(UPLOAD_DIR, f"{int(datetime.utcnow().timestamp())}_{filename}")
    with open(saved_path, "wb") as f:
        f.write(await file.read())

    try:
        text = extract_text_from_pdf(saved_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    parsed = parse_po_details(text)
    po_number = parsed.get("po_number")
    po_date = parsed.get("po_date")
    total_amount = parsed.get("total_amount")

    if not po_number:
        raise HTTPException(status_code=400, detail="PO Number not found in document")

    po_in = PurchaseOrderCreate(
        po_number=po_number,
        po_date=po_date,
        total_amount=total_amount,
        file_path=saved_path
    )

    try:
        po = create_purchase_order(db, po_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return po


@router.post("/purchase_order")
def list_purchase_orders(schema: PurchaseOrderFilter, db: Session = Depends(get_db)):
    return get_purchase_orders(schema, db)


