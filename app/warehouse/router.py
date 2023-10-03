from typing import Annotated
from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.orm import Session

from ..database import get_pg_db
from ..user.auth import Auth
from . import db_warehouse, db_stock
from .schemas import WarehouseDisplay, WarehouseCreateBase, StockCreatebase, ModifyStock
from ..user.schemas import UserDisplay

router = APIRouter(
    prefix='/warehouse',
    tags=['warehouse']
)

@router.post('/', response_model=WarehouseDisplay)
async def create_warehouse(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: WarehouseCreateBase = Body()
):
    return db_warehouse.create_warehouse(db, request)

@router.get('/{warehouse_id}/stock')
async def get_warehouse_stock(
    db: Annotated[Session, Depends(get_pg_db)],
    warehouse_id: int = Path(..., ge=1)
):
    return db_stock.get_warehouse_stock(db, warehouse_id)

@router.post('/{warehouse_id}/stock/{product_id}')
async def create_stock(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: StockCreatebase = Body(),
    warehouse_id: int = Path(..., ge=1),
    product_id: str = Path(..., min_length=6, max_length=6)
):
    return db_stock.create_stock(
        db, product_id, warehouse_id, request.units_in_stock
    )

@router.patch('/{warehouse_id}/stock/{product_id}')
async def modify_stock(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: ModifyStock = Body(),
    warehouse_id: int = Path(..., ge=1),
    product_id: str = Path(..., min_length=6, max_length=6)
):
    return db_stock.add_stock(
        db, product_id, warehouse_id, request.modifier
    )

@router.put('/{warehouse_id}/stock/{product_id}')
async def set_stock(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: StockCreatebase = Body(),
    warehouse_id: int = Path(..., ge=1),
    product_id: str = Path(..., min_length=6, max_length=6)
):
    return db_stock.set_stock(
        db, product_id, warehouse_id, request.units_in_stock
    )
