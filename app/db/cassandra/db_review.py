from cassandra.cluster import Session
from uuid import UUID
from datetime import datetime

from ...db.cassandra.models import DbReview
from ...schemas.review import ReviewCreateBase

def create_review(db: Session, id: UUID, product_number: int, request: ReviewCreateBase):
    publication_datetime = datetime.now()
    
    review = DbReview.create(
        product_number=product_number,
        publication_datetime=publication_datetime,
        description = request.description, 
        rating=request.rating,
        user_id=id
    )
    
    return review