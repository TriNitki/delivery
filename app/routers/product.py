from typing import Annotated
from fastapi import APIRouter, Depends
import sqlalchemy.orm.session as sqlalchemy

from ..db.database import get_pg_db
from ..db.jwt import JwtHandler
from ..db.postgres import db_product
from ..schemas.product import ProductCreateBase, ProductDisplay
from ..schemas.user import UserDisplay


router = APIRouter(
    prefix='/product',
    tags=['product']
)

@router.post('/', response_model=ProductDisplay)
async def create_product(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    request: ProductCreateBase,
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)]
):
    return db_product.create_product(db, current_user.id, request)

@router.get('/{product_id}', response_model=ProductDisplay)
async def retrieve_product(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str,
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)]
):
    return db_product.retrieve_product(db, product_id)
    