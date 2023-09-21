from sqlalchemy.orm.session import Session
from fastapi import HTTPException

from ..models import DbStock

def create_stock(db: Session, product_id: str, warehouse_id: int, quantity: int):
    new_stock = DbStock(
        product_id=product_id,
        warehouse_id=warehouse_id,
        units_in_stock=quantity
    )
    
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock

def get_stock(db: Session, product_id: str):
    products = db.query(DbStock).filter(DbStock.product_id == product_id).all()
    return products

def add_stock(db: Session, product_id: str, warehouse_id: int, modifier: int):
    product = db.query(DbStock).filter(
        DbStock.product_id == product_id, DbStock.warehouse_id == warehouse_id
    )
    
    if product.one().units_in_stock + modifier < 0:
        raise HTTPException(
            status_code=400,
            detail='The value of the number of products in stock cannot be lower than 0'
        )
    
    product.update({
        DbStock.units_in_stock: DbStock.units_in_stock + modifier
    })
    db.commit()
    
    return product.one()

def set_stock(db: Session, product_id: str, warehouse_id: int, quantity: int):
    if quantity < 0:
        raise HTTPException(
            status_code=400,
            detail='The value of the number of products in stock cannot be lower than 0'
        )
    product = db.query(DbStock).filter(
        DbStock.product_id == product_id, DbStock.warehouse_id == warehouse_id
    )
    
    product.update({
        DbStock.units_in_stock: quantity
    })
    db.commit()
    
    return product.one()