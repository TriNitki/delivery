from sqlalchemy.orm.session import Session
import uuid

from ...schemas.user import UserCreateBase, UserUpdateBase
from .models import DbUser

def create_user(db: Session, request: UserCreateBase) -> DbUser:
    new_user = DbUser(
        full_name = request.full_name,
        email = request.email,
        phone_number = request.phone_number,
        gender = request.gender,
        date_of_birth = request.date_of_birth,
        city = request.city,
        profile_picture = request.profile_picture,
        password = request.password,
        currency_name = request.currency_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, id: uuid.UUID, request: UserUpdateBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    
    for attr, value in request.model_dump().items():
        if value is not None:
            user.update({
                getattr(DbUser, attr): value
            })
    
    db.commit()
    return user.one()

def deactivate_user(db: Session, id: uuid.UUID):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update({DbUser.is_active: False})
    
    db.commit()

def get_user_by_email(db: Session, email: str):
    return db.query(DbUser).filter_by(email=email).first()