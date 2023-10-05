from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from ..models import DbStock

def create_stock(db: Session, product_id: str, warehouse_id: int, quantity: int):
    new_stock = DbStock(
        product_id=product_id,
        warehouse_id=warehouse_id,
        units_in_stock=quantity
    )
    
    db.add(new_stock)
    
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=403,
            detail="Product's stock already exists in this warehouse"
        )
    
    db.refresh(new_stock)
    return new_stock

def get_product_stock(db: Session, product_id: str):
    stock = db.query(DbStock).filter(DbStock.product_id == product_id)
    return stock.all()

def get_warehouse_stock(db: Session, warehouse_id: int):
    stock = db.query(DbStock).filter(DbStock.warehouse_id == warehouse_id)
    return stock.all()

def get_product_warehouse_stock(db: Session, product_id: str, warehouse_id: int):
    stock = db.query(DbStock).filter(
        DbStock.product_id == product_id, 
        DbStock.warehouse_id == warehouse_id
    )
    return stock.one()

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