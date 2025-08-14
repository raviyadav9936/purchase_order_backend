from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional


class PurchaseOrderCreate(BaseModel):
    po_number: str
    po_date: Optional[date]
    total_amount: Optional[float]
    uploaded_at: Optional[datetime] = None
    file_path: Optional[str]


class PurchaseOrderOut(BaseModel):
    id: int
    po_number: str
    po_date: Optional[date]
    total_amount: Optional[float]
    uploaded_at: Optional[datetime]
    file_path: Optional[str]

    class Config:
        orm_mode = True

class PurchaseOrderFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @validator("start_date", "end_date", pre=True)
    def empty_str_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

