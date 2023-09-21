from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from ..database import get_pg_db
from ..user.auth import Auth
from .schemas import ReviewCreateBase, ReviewDisplay
from ..user.schemas import UserDisplay
from . import db_review


router = APIRouter(
    prefix='/product/{product_id}/review',
    tags=['review']
)


@router.post('/', response_model=ReviewDisplay)
async def create_review(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path(),
    request: ReviewCreateBase = Body()
):
    return db_review.create_review(db, current_user.id, product_id, request)