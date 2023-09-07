from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body

from ..utils.auth import Auth
from ..schemas.review import ReviewCreateBase, ReviewDisplay
from ..schemas.user import UserDisplay
from ..db.cassandra import db_review


router = APIRouter(
    prefix='/product/{product_id}/review',
    tags=['review']
)



@router.post('/', response_model=ReviewDisplay)
async def create_review(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    product_id: str = Path(),
    request: ReviewCreateBase = Body()
):
    return db_review.create_review(current_user.id, product_id, request)