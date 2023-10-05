from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from ..database import get_pg_db
from ..user.auth import Auth
from .schemas import ReviewCreateBase, ReviewDisplay, ReviewUpdateBase
from ..user.schemas import UserDisplay
from . import db_review


router = APIRouter(
    prefix='/product/{product_id}',
    tags=['review']
)


@router.post('/review', response_model=ReviewDisplay)
async def create_review(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path(),
    request: ReviewCreateBase = Body()
):
    return db_review.create_review(db, current_user.id, product_id, request)

@router.get('/reviews', response_model=List[ReviewDisplay])
async def get_reviews(
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_review.get_reviews(db, product_id)

@router.patch('/review', response_model=ReviewDisplay)
async def update_review(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path(),
    request: ReviewUpdateBase = Body()
):
    return db_review.update_review(db, current_user.id, product_id, request)

@router.delete('/review', response_model=None)
async def delete_review(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_review.delete_review(db, current_user.id, product_id)