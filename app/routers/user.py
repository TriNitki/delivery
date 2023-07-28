from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import sqlalchemy.orm.session as sqlalchemy

from ..db.database import get_pg_db
from ..db.postgres import db_user
from ..db.jwt import JwtHandler
from ..schemas.user import UserCreateBase, UserDisplay, UserUpdateBase
from ..schemas.token import Token


router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/signin', response_model=UserDisplay)
async def signup(
    request: UserCreateBase, 
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)]
):
    return db_user.create_user(db, request)
     

@router.post('/login', response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)]
):
    access_token = await JwtHandler.generate_token(db, form_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserDisplay)
async def user_me(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)]
):
    return current_user

@router.patch('/edit', response_model=UserDisplay)
async def user_edit(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    request: UserUpdateBase,
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)]
):
    return db_user.update_user(db, current_user.id, request)

@router.delete('/delete', response_model=None)
async def user_deactivate(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    db: Annotated[sqlalchemy.Session, Depends(get_pg_db)]
):
    db_user.update_user(db, current_user.id, UserUpdateBase(is_active=False))
    return None