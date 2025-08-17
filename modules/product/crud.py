from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database.models import Product,Order


def add_product(schema,db):
    try:
        existing_product=db.query(Product).filter(Product.name==schema.name).first()
        if existing_product:
            raise HTTPException(status_code=400,detail='Product with this name already exists')
        
        new_product=Product(
            name=schema.name,
            price=schema.price,
            stock_qty=schema.stock_qty
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "status":True,
            "message":"Product added successfully",
            "data":{
                'id':new_product.id,
                'name':new_product.name,
                'price':new_product.price,
                'stock_qty':new_product.stock_qty
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        return {'status': False, 'message': 'Something went wrong'}


def place_order(schema, db: Session):
    try:
        product = db.query(Product).filter(Product.id == schema.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.stock_qty < schema.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        total_price = product.price * schema.quantity

        product.stock_qty -= schema.quantity

        new_order = Order(
            product_id=schema.product_id,
            quantity=schema.quantity,
            total_price=total_price,
            order_date=datetime.utcnow() 
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return {
            "status": True,
            "message": "Order placed successfully",
            "data": {
                "order_id": new_order.id,
                "product_id": new_order.product_id,
                "quantity": new_order.quantity,
                "total_price": new_order.total_price,
                "remaining_stock": product.stock_qty,
                "order_date": new_order.order_date.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        return {"status": False, "message": "Something went wrong"}


def get_top_products(db):
    try:
        top_products = (
            db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(Order.quantity).label("total_quantity_sold")
            )
            .join(Order, Product.id == Order.product_id)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(Order.quantity).desc())
            .limit(10)
            .all()
        )

        result = [
            {
                "product_id": row.product_id,
                "product_name": row.product_name,
                "total_quantity_sold": row.total_quantity_sold
            }
            for row in top_products
        ]
        # return result
        return {
            'status':True,
            'message':'Product fetch successfully',
            'data': result
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        return {"status": False, "message": "Something went wrong"}

















