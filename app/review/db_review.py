from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import DbReview
from .schemas import ReviewCreateBase, ReviewUpdateBase

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

def get_reviews(db: Session, product_id: str):
    reviews = db.query(DbReview).filter(DbReview.product_id == product_id)
    return reviews.all()

def update_review(db: Session, user_id: UUID, product_id: str, request: ReviewUpdateBase):  # noqa: E501
    review = db.query(DbReview).filter(
        DbReview.product_id == product_id, 
        DbReview.user_id == user_id
    )
    
    for attr, value in request.model_dump().items():
        if value is not None:
            review.update({
                getattr(DbReview, attr): value
            })
    
    db.commit()
    return review.one()

def delete_review(db: Session, user_id: UUID, product_id: str):
    review = db.query(DbReview).filter(
        DbReview.product_id == product_id, 
        DbReview.user_id == user_id
    )
    review.delete()
    db.commit()
    return None