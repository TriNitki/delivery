from fastapi import APIRouter, Depends, HTTPException, Cookie, Body
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from redis import Redis

from ..utils.auth import Auth
from ..db.database import get_pg_db, get_rds_db
from ..db.postgres import db_user
from ..schemas.user import UserCreateBase, UserDisplay, UserUpdateBase
from ..schemas.token import Token
from ..config import settings

router = APIRouter(
    prefix='/user',
    tags=['user']
)

security = HTTPBearer()


@router.post('/signup', response_model=UserDisplay)
async def signup(
    db: Annotated[Session, Depends(get_pg_db)],
    request: UserCreateBase = Body()
):
    if request.password != request.password_confirm:
        raise HTTPException(400, 'Password and password confirmation are not the same')
    
    del request.password_confirm
    
    if db_user.get_user_by_email(db, request.email):
        raise HTTPException(409, 'Account already exist')
    
    encoded_password = await Auth.encode_password(request.password)
    
    request.password = encoded_password
    
    user = db_user.create_user(db, request)
    return user

@router.post('/login', response_model=Token)
async def login(
    db: Annotated[Session, Depends(get_pg_db)],
    redis_db: Annotated[Redis, Depends(get_rds_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await Auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(401, 'Invalid email or password')
    access_token = await Auth.encode_access_token(user.email, user.id, user.role)
    refresh_token = await Auth.encode_refresh_token(user.email, user.id, user.role)
    
    content = {'access_token': access_token, 'token_type': 'bearer'}
    response = JSONResponse(content=content)
    response.set_cookie(key="refresh_token", value=refresh_token)
    
    redis_db.set(str(user.id), refresh_token, ex=settings.REFRESH_TOKEN_EXPIRE_MINUTES*60)
    
    return response

@router.post('/refresh', response_model=Token)
async def refresh_token(
    redis_db: Annotated[Redis, Depends(get_rds_db)],
    refresh_token: Annotated[str, Cookie(min_length=1)] = None
):
    new_access_token, new_refresh_token = await Auth.refresh_token(refresh_token)
    
    payload = await Auth.decode_access_token(new_access_token)
    old_refresh_token = redis_db.get(payload['id'])
    
    if old_refresh_token != refresh_token:
        raise HTTPException(401, 'Invalid token')
    
    content = {'access_token': new_access_token, 'token_type': 'bearer'}
    response = JSONResponse(content=content)
    response.set_cookie(key="refresh_token", value=new_refresh_token)
    
    redis_db.set(payload['id'], new_refresh_token, ex=settings.REFRESH_TOKEN_EXPIRE_MINUTES*60)
    
    return response

@router.get("/me", response_model=UserDisplay)
def user_me(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)]
):
    return current_user

@router.patch('/me', response_model=UserDisplay)
def user_edit(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: UserUpdateBase = Body()
    
):
    return db_user.update_user(db, current_user.id, request)

@router.delete('/me', response_model=None)
def user_deactivate(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)]
):
    db_user.update_user(db, current_user.id, UserUpdateBase(is_active=False))
    return None