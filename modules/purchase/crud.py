from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import PurchaseOrder
from modules.purchase.schema import PurchaseOrderCreate
from datetime import date,datetime
from sqlalchemy import cast, Date
from typing import Optional


def create_purchase_order(db: Session, po_in: PurchaseOrderCreate):
    try:
        po = PurchaseOrder(
            po_number=po_in.po_number,
            po_date=po_in.po_date,
            total_amount=po_in.total_amount,
            uploaded_at=po_in.uploaded_at,
            file_path=po_in.file_path
        )
        db.add(po)
        db.commit()
        db.refresh(po)
        return po  

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong")


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
                "uploaded_at": po.uploaded_at
            }
            for po in purchase_orders
        ]

        return {"status": True, "message": "Data fetched successfully", "data": result}

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        return {"status": False, "message": "Something went wrong", "data": []}