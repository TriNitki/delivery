from pydantic import BaseModel, Field
from datetime import datetime

from ..user.schemas import MinUserDisplay

class ReviewCreateBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    description: str
    
class ReviewUpdateBase(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    description: str | None
    
class ReviewDisplay(BaseModel):
    product_id: str
    rating: int
    description: str
    publication_datetime: datetime
    reviewer: MinUserDisplay

class ReviewTestModel(BaseModel):
    product_id: str | None = None
    rating: int | None = None
    description: str | None = None
    publication_datetime: datetime | None = None
    user_id: MinUserDisplay | None = None