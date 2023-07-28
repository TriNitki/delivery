from typing import Annotated
from fastapi import APIRouter, Depends
import cassandra.cluster as cassandra

from ..db.database import get_ac_db
from ..db.jwt import JwtHandler
from ..schemas.review import ReviewCreateBase, ReviewDisplay
from ..schemas.user import UserDisplay
from ..db.cassandra import db_review


router = APIRouter(
    prefix='/product/{product_number}/review',
    tags=['review']
)

@router.post('/', response_model=ReviewDisplay)
async def create_review(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_number: int,
    request: ReviewCreateBase,
    db: Annotated[cassandra.Session, Depends(get_ac_db)]
):
    return db_review.create_review(db, current_user.id, product_number, request)