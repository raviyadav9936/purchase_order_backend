from sqlalchemy import Date, DateTime, ForeignKey, Integer,String,Column,Float, func,Text
from database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Float)
    stock_qty = Column(Integer)

    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="orders")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(255), index=True, nullable=False)
    po_date = Column(Date, index=True, nullable=True)
    vendor_name=Column(String(255))
    total_amount = Column(Float, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String(1024))