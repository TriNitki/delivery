from fastapi import HTTPException, Depends
from sqlalchemy.orm.session import Session
from datetime import datetime
from typing import List

from .database import get_pg_db
from .product import db_product
from .user import db_user
from .warehouse import db_warehouse
from .order import db_order
from .order.schemas import OrderDetails, OrderProductCreateBase
from .user.schemas import MinUserDisplay
from .warehouse.schemas import WarehouseDisplay

def valid_product_id(
    product_id: str,
    db: Session = Depends(get_pg_db)
):
    if len(product_id) != 6:
        raise HTTPException(
            status_code=400,
            detail="Incorrect product ID format"
        )
    
    product = db_product.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product with this ID was not found"
        )
    
    return product

def valid_order_details(
    order_details: List[OrderProductCreateBase],
    db: Session = Depends(get_pg_db)
):
    details = []
    for detail in order_details:
        product_ = valid_product_id(detail.product_id, db)
        seller_ = db_user.get_user_by_id(db, product_.seller_id)
        warehouse_ = db_warehouse.get_warehouse(db, detail.warehouse_id)
        
        seller = MinUserDisplay(**seller_.__dict__)
        warehouse = WarehouseDisplay(**warehouse_.__dict__)
        
        
        details.append(
            OrderDetails(
                quantity=detail.quantity,
                estimated_delivery_time=warehouse.packaging_time,
                delivery_datetime=datetime.utcnow() + warehouse.packaging_time,
                is_cancelled=False,
                **product_.__dict__,
                warehouse=warehouse,
                seller=seller
            )
        )
    
    return details

def valid_order(
    order_id: str,
    db: Session = Depends(get_pg_db)
):
    order = db_order.get_order(db, order_id)
    
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order with this ID was not found"
        )
    
    return order