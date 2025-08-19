import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from database.models import PurchaseOrder
from modules.purchase.schema import PurchaseOrderCreate
from datetime import date,datetime
from sqlalchemy import cast, Date
from typing import Optional
from modules.purchase.utils import extract_text_from_pdf, parse_po_details  

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:
    filename = file.filename
    if not (filename.lower().endswith(".pdf") or filename.lower().endswith((".png", ".jpg", ".jpeg"))):
        raise HTTPException(status_code=400, detail="Only PDF / PNG / JPG files supported")

    saved_path = os.path.join(UPLOAD_DIR, f"{int(datetime.utcnow().timestamp())}_{filename}")
    with open(saved_path, "wb") as f:
        f.write(file.file.read()) 
    return saved_path


def create_purchase_order(db: Session, po_in: PurchaseOrderCreate):
    try:
        po = PurchaseOrder(
            po_number=po_in.po_number,
            po_date=po_in.po_date,
            vendor_name=po_in.vendor_name,
            total_amount=po_in.total_amount,
            uploaded_at=po_in.uploaded_at,
            file_path=po_in.file_path
        )

        db.add(po)
        db.commit()
        db.refresh(po)
        return po
    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong")


def process_and_create_po(file: UploadFile, db: Session):
    saved_path = save_uploaded_file(file)

    try:
        text = extract_text_from_pdf(saved_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    parsed = parse_po_details(text)
    po_number = parsed.get("po_number")
    po_date = parsed.get("po_date")
    vendor_name=parsed.get('vendor_name')
    total_amount = parsed.get("total_amount")

    if not po_number:
        raise HTTPException(status_code=400, detail="PO Number not found in document")

    po_in = PurchaseOrderCreate(
        po_number=po_number,
        po_date=po_date,
        vendor_name=vendor_name,
        total_amount=total_amount,
        file_path=saved_path,
    )

    return create_purchase_order(db, po_in)



def get_purchase_orders(start_date: date, end_date: date, db: Session):
    try:
        query = db.query(PurchaseOrder)

        if start_date and end_date and start_date == end_date:
            query = query.filter(PurchaseOrder.po_date == start_date)
        elif start_date and end_date:
            query = query.filter(PurchaseOrder.po_date.between(start_date, end_date))
        elif start_date:
            query = query.filter(PurchaseOrder.po_date >= start_date)
        elif end_date:
            query = query.filter(PurchaseOrder.po_date <= end_date)

        purchase_orders = query.order_by(PurchaseOrder.po_date.desc()).all()

        result = [
            {
                "id": po.id,
                "po_number": po.po_number,
                "po_date": po.po_date,
                "total_amount": po.total_amount,
                "uploaded_at": po.uploaded_at,
                'vendor_name':po.vendor_name
            }
            for po in purchase_orders
        ]

        return {"status": True, "message": "Data fetched successfully", "data": result}

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        return {"status": False, "message": "Something went wrong", "data": []}