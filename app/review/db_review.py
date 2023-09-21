from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import DbReview
from .schemas import ReviewCreateBase

def create_review(db: Session, id: UUID, product_id: str, request: ReviewCreateBase):
    publication_datetime = datetime.utcnow()
    
    new_review = DbReview(
        product_id=product_id,
        publication_datetime=publication_datetime,
        description = request.description, 
        rating=request.rating,
        user_id=id
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review