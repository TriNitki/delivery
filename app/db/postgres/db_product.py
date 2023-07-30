from sqlalchemy.orm.session import Session
import uuid

from ...schemas.product import ProductCreateBase
from ...db.postgres.models import DbProduct

def create_product(db: Session, id: uuid.UUID, request: ProductCreateBase):
    new_product = DbProduct(
        product_number = None,
        price = request.price,
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
    return new_product