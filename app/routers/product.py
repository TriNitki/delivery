from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body
import sqlalchemy.orm.session as sqlalchemy

from ..db.database import get_pg_db
from ..utils.auth import Auth
from ..db.postgres import db_product
from ..db.elastic import product_autocomplete as product_ac
from ..schemas.product import ProductCreateBase, ProductDisplay
from ..schemas.user import UserDisplay


router = APIRouter(
    prefix='',
    tags=['product']
)

@router.post('/product/', response_model=ProductDisplay)
async def create_product(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)],
    request: ProductCreateBase = Body()
):
    new_product = db_product.create_product(db, current_user.id, request)
    product_ac.add_product(new_product)
    return new_product

@router.get('/product/{product_id}', response_model=ProductDisplay)
async def get_product(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_product.get_product(db, product_id)

