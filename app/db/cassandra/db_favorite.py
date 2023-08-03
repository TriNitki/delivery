from uuid import UUID
from datetime import datetime

from .models import DbFavorite

def create_favorite(id: UUID, product_id: str):
    addition_datetime = datetime.now()
    
    new_favorite = DbFavorite.create(
        product_id=product_id,
        user_id=id,
        addition_datetime=addition_datetime
    )
    
    return new_favorite