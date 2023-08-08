from sqlalchemy.orm.session import Session
import uuid

from ...schemas.user import UserCreateBase, UserUpdateBase, LoginBase
from .models import DbUser
from ...utils.hash import Hash

def create_user(db: Session, request: UserCreateBase) -> DbUser:
    hashed_password = Hash.bcrypt(request.password)
    new_user = DbUser(
        full_name = request.full_name,
        email = request.email,
        phone_number = request.phone_number,
        gender = request.gender,
        date_of_birth = request.date_of_birth,
        city = request.city,
        profile_picture = request.profile_picture,
        password = hashed_password,
        currency_name = request.currency_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, id: uuid.UUID, request: UserUpdateBase) -> DbUser:
    user = db.query(DbUser).filter(DbUser.id == id)
    
    for attr, value in request.model_dump().items():
        if value is not None:
            user.update({
                getattr(DbUser, attr): value
            })
    
    db.commit()
    return user.one()

def get_user_by_email(db: Session, email: str) -> DbUser:
    return db.query(DbUser).filter_by(email=email).first()

def authenticate_user(db: Session, email: str, plain_password: str) -> DbUser:
    user = get_user_by_email(db, email)
    if not user:
        return False
    
    hashed_password = user.password
    if not Hash.verify(hashed_password, plain_password):
        return False
    return user