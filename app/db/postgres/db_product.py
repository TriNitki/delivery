from sqlalchemy.orm.session import Session
import uuid

from ...schemas.product import ProductCreateBase, ProductDisplay
from ...db.postgres.models import DbProduct, DbStock
from .db_stock import create_stock


def create_product(db: Session, id: uuid.UUID, request: ProductCreateBase):
    new_product = DbProduct(
        price = request.price,
        name = request.name,
        weight = request.weight,
        manufacturer_country = request.manufacturer_country.value,
        category_name = request.category_name,
        brand = request.brand,
        discount = request.discount,
        description = request.description,
        image =  request.image,
        seller_id = id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    create_stock(db, new_product.id, request.stock.warehouse_id, request.stock.units_in_stock)
    
    return new_product

def get_product(db: Session, product_id: str) -> ProductDisplay:
    return db.query(DbProduct).filter(DbProduct.id == product_id).first()