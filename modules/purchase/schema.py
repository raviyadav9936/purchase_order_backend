from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional


class PurchaseOrderCreate(BaseModel):
    po_number: str
    po_date: Optional[date]
    vendor_name:Optional[str]=None
    total_amount: Optional[float]
    uploaded_at: Optional[datetime] = None
    file_path: Optional[str]


class PurchaseOrderOut(BaseModel):
    id: int
    po_number: str
    po_date: Optional[date]
    vendor_name:Optional[str]
    total_amount: Optional[float]
    uploaded_at: Optional[datetime]
    file_path: Optional[str]

    class Config:
        orm_mode = True


