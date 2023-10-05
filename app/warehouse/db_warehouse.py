from sqlalchemy.orm.session import Session

from .schemas import WarehouseCreateBase, WarehouseUpdateBase
from ..models import DbWarehouse

def create_warehouse(db: Session, request: WarehouseCreateBase):
    new_warehouse = DbWarehouse(
        address = request.address,
        packaging_time = request.packaging_time
    )
    
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    return new_warehouse

def get_warehouse(db: Session, id: int):
    return db.query(DbWarehouse).filter(DbWarehouse.id == id).one()

def update_warehouse(db: Session, id: int, request: WarehouseUpdateBase):
    warehouse = db.query(DbWarehouse).filter(DbWarehouse.id == id)
    
    for attr, value in request.model_dump().items():
        if value is not None:
            warehouse.update({
                getattr(DbWarehouse, attr): value
            })
    
    db.commit()
    return warehouse.one()