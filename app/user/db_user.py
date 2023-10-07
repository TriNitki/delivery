from sqlalchemy.orm.session import Session
import uuid

from .schemas import UserCreateBase, UserUpdateBase
from ..models import DbUser

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

def update_status(db: Session, id: uuid.UUID, status: bool):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update({DbUser.is_active: status})
    
    db.commit()

def get_user_by_id(db: Session, id: uuid.UUID):
    return db.query(DbUser).filter(DbUser.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(DbUser).filter_by(email=email).first()