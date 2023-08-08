from uuid import UUID
from datetime import datetime

from .models import DbFavorite

def create_favorite(id: UUID, product_id: str):
    addition_datetime = datetime.utcnow()
    
    new_favorite = DbFavorite.create(
        product_id=product_id,
        user_id=id,
        addition_datetime=addition_datetime
    )
    
    return new_favorite

def get_user_favorites(id: UUID):
    favorites = DbFavorite.objects(user_id = id).all()[:]
    return {
        "user_id": id,
        "favorites": [{
            "product_id": favorite["product_id"],
            "addition_datetime": favorite["addition_datetime"]
            } for favorite in favorites]
    }