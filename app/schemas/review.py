from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ReviewCreateBase(BaseModel):
    rating: int
    description: str
    
class ReviewDisplay(BaseModel):
    product_number: int
    rating: int
    description: str
    publication_datetime: datetime
    user_id: UUID