from uuid import UUID
from datetime import datetime

from .models import DbReview
from ...schemas.review import ReviewCreateBase

def create_review(id: UUID, product_id: str, request: ReviewCreateBase):
    publication_datetime = datetime.now()
    
    new_review = DbReview.create(
        product_id=product_id,
        publication_datetime=publication_datetime,
        description = request.description, 
        rating=request.rating,
        user_id=id
    )
    
    return new_review