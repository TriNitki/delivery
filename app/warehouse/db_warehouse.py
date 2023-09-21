from sqlalchemy.orm.session import Session

from .schemas import WarehouseCreateBase
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