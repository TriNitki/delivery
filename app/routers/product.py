from typing import Annotated
from fastapi import APIRouter, Depends

from ..db.database import get_pg_db

router = APIRouter(
    prefix='/product',
    tags=['product']
)

@router.post('/')
def create_user():
    pass