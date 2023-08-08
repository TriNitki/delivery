from fastapi import APIRouter, Depends, Path, Query, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import sqlalchemy.orm.session as sqlalchemy

from ..db.database import get_pg_db
from ..db.postgres import db_user
from ..utils.auth import Auth
from ..schemas.user import UserCreateBase, UserDisplay, UserUpdateBase
from ..schemas.token import Token


router = APIRouter(
    prefix='/user',
    tags=['user']
)

auth_handler = Auth()

@router.post('/signin', response_model=UserDisplay)
async def signup(
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)],
    request: UserCreateBase = Body()
):
    return db_user.create_user(db, request)
     

@router.post('/login', response_model=Token)
async def login(
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    
):
    access_token = await JwtHandler.generate_access_token(db, form_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserDisplay)
async def user_me(
    current_user: Annotated[UserDisplay, Depends(auth_handler.get_current_active_user)]
):
    return current_user

@router.patch('/me', response_model=UserDisplay)
async def user_edit(
    current_user: Annotated[UserDisplay, Depends(auth_handler.get_current_active_user)],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)],
    request: UserUpdateBase = Body()
    
):
    return db_user.update_user(db, current_user.id, request)

@router.delete('/me', response_model=None)
async def user_deactivate(
    current_user: Annotated[UserDisplay, Depends(auth_handler.get_current_active_user)],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)]
):
    db_user.update_user(db, current_user.id, UserUpdateBase(is_active=False))
    return None