from sqlalchemy.orm.session import Session
import uuid

from .schemas import ProductCreateBase
from ..models import DbProduct


def create_product(db: Session, seller_id: uuid.UUID, request: ProductCreateBase):
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
        seller_id = seller_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

def get_product(db: Session, product_id: str):
    return db.query(DbProduct).filter(DbProduct.id == product_id).first()

def get_products(db: Session, product_ids: list):
    return db.query(DbProduct).filter(DbProduct.id.in_(product_ids)).all()