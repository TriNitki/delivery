from typing import Annotated
from fastapi import APIRouter, Depends, Body
import sqlalchemy.orm.session as sqlalchemy

from ..db.database import get_pg_db
from ..utils.auth import Auth
from ..db.postgres import db_warehouse
from ..schemas.warehouse import WarehouseDisplay, WarehouseCreateBase
from ..schemas.user import UserDisplay

router = APIRouter(
    prefix='/warehouse',
    tags=['warehouse']
)



@router.post('/', response_model=WarehouseDisplay)
async def create_warehouse(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)],
    request: WarehouseCreateBase = Body()
    
):
    return db_warehouse.create_warehouse(db, request)

