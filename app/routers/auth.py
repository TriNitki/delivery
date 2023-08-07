from datetime import timedelta
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from pydantic import EmailStr

from ..schemas.user import UserCreateBase, LoginBase, UserDisplay
from sqlalchemy.orm import Session
from ..db.database import get_pg_db
from ..db.postgres import db_user
from ..config import settings
from ..utils.hash import Hash


router = APIRouter(
    prefix='/',
    tags=['auth']
)

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRE_MINUTES

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserDisplay)
async def create_user(payload: UserCreateBase, db: Session = Depends(get_pg_db)):
    user = db_user.get_user_by_email(db, payload.email.lower())
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    
    if payload.password != payload.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    
    payload.password = Hash.bcrypt(payload.password)
    del payload.password_confirm
    payload.email = EmailStr(payload.email.lower())
    
    return db_user.create_user(db, payload)
    
    