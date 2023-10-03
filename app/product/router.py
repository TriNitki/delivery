from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from ..database import get_pg_db
from ..user.auth import Auth
from . import db_product, db_stock
from ..search import product_autocomplete as product_ac
from .schemas import (ProductCreateBase, ProductDisplay, StockCreatebase, 
                      ProductUpdateBase, ModifyStock, SetStatus)
from ..user.schemas import UserDisplay


router = APIRouter(
    prefix='',
    tags=['product']
)

@router.post('/product/', response_model=ProductDisplay)
async def create_product(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: ProductCreateBase = Body()
):
    new_product = db_product.create_product(db, current_user.id, request)
    product_ac.add_product(new_product)
    return new_product

@router.patch('/product/{product_id}', response_model=ProductDisplay)
async def update_product(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: ProductUpdateBase = Body(),
    product_id: str = Path()
):
    updated_product = db_product.update_product(db, current_user.id, product_id, request)  # noqa: E501
    # product_ac.add_product(new_product)
    return updated_product

@router.get('/product/{product_id}', response_model=ProductDisplay)
async def get_product(
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_product.get_product(db, product_id)

@router.put('/product/{product_id}/status', response_model=None)
async def set_status(
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path(),
    request: SetStatus = Body()
):
    return db_product.set_status(db, product_id, request.is_active)

@router.get('/product/{product_id}/stock')
async def get_stock(
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_stock.get_stock(db, product_id)

@router.post('/product/{product_id}/stock')
async def create_stock(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: StockCreatebase = Body(),
    product_id: str = Path()
):
    return db_stock.create_stock(
        db, product_id, request.warehouse_id, request.units_in_stock
    )

@router.patch('/product/{product_id}/stock')
async def modify_stock(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: ModifyStock = Body(),
    product_id: str = Path(),
):
    return db_stock.add_stock(
        db, product_id, request.warehouse_id, request.modifier
    )

@router.put('/product/{product_id}/stock')
async def set_stock(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: StockCreatebase = Body(),
    product_id: str = Path()
):
    return db_stock.set_stock(
        db, product_id, request.warehouse_id, request.units_in_stock
    )
