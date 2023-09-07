from sqlalchemy.orm.session import Session

from ...db.postgres.models import DbStock

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

def add_stock(db: Session, product_id: str, quantity: int):
    product = db.query(DbStock).filter(DbStock.product_id == product_id)
    product.update({
        DbStock.units_in_stock: DbStock.units_in_stock + quantity
    })
    db.commit()
    return

def subtract_stock(db: Session, product_id: str, quantity: int):
    product = db.query(DbStock).filter(DbStock.product_id == product_id)
    product.update({
        DbStock.units_in_stock: DbStock.units_in_stock - quantity
    })
    db.commit()
    return