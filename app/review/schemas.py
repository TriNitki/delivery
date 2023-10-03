from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ReviewCreateBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    description: str
    
class ReviewDisplay(BaseModel):
    product_id: str
    rating: int
    description: str
    publication_datetime: datetime
    user_id: UUID