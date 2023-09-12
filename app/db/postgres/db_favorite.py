from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from fastapi import HTTPException

from .models import DbFavorite

def create_favorite(db: Session, user_id: UUID, product_id: str):
    new_favorite = DbFavorite(
        user_id = user_id,
        product_id = product_id
    )
    
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    
    return new_favorite

def delete_favorite(db: Session, user_id: UUID, product_id: str):
    favorite = db.query(DbFavorite).filter(
        and_(DbFavorite.user_id == user_id, DbFavorite.product_id == product_id)
    ).first()
    if not favorite:
        raise HTTPException(
            status_code=404,
            detail='The favorited product was not found '
        )
    
    db.delete(favorite)
    db.commit()