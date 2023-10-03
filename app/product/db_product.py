from sqlalchemy.orm.session import Session
import uuid
from fastapi import HTTPException

from .schemas import ProductCreateBase, ProductUpdateBase
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
        image = request.image,
        seller_id = seller_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

def update_product(
    db: Session, seller_id: uuid.UUID, product_id: str, request: ProductUpdateBase
):
    product = db.query(DbProduct).filter(DbProduct.id == product_id)
    
    if product.one().seller_id != seller_id:
        raise HTTPException(
            status_code=403,
            detail='You do not have permission to update this product'
        )
    
    for attr, value in request.model_dump().items():
        if value is not None:
            product.update({
                getattr(DbProduct, attr): value
            })
    
    db.commit()
    return product.one()

def get_product(db: Session, product_id: str):
    return db.query(DbProduct).filter(DbProduct.id == product_id).first()

def set_status(db: Session, product_id: str, status: bool):
    product = db.query(DbProduct).filter(DbProduct.id == product_id)
    product.update({DbProduct.is_active: status})
    
    db.commit()
    return None