from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body
import sqlalchemy.orm.session as sqlalchemy

from ..db.database import get_pg_db
from ..utils.auth import Auth
from ..db.postgres import db_product
from ..schemas.product import ProductCreateBase, ProductDisplay, ProductSearchResult
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
    return db_product.create_product(db, current_user.id, request)

@router.get('/product/{product_id}', response_model=ProductDisplay)
async def get_product(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_product.get_product(db, product_id)