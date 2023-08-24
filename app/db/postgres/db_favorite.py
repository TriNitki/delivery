from uuid import UUID
from sqlalchemy.orm.session import Session

from .models import DbFavorite, DbUser

def create_favorite(db: Session, user_id: UUID, product_id: str):
    new_favorite = DbFavorite(
        user_id = user_id,
        product_id = product_id
    )
    
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    
    return new_favorite

def get_favorites_by_user(db: Session, user_id: UUID):
    return db.query(DbUser).filter(DbUser.id == user_id).first()