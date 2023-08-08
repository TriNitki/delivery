from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from ..utils.auth import Auth
from ..db.database import get_pg_db
from ..db.postgres import db_user
from ..schemas.user import UserCreateBase, UserDisplay
from ..schemas.token import Token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

security = HTTPBearer()


@router.post('/signup', response_model=UserDisplay)
async def signup(
    db: Annotated[Session, Depends(get_pg_db)],
    request: UserCreateBase
):
    if request.password != request.password_confirm:
        raise HTTPException(400, 'Password and password confirmation are not the same')
    
    del request.password_confirm
    
    if db_user.get_user_by_email(db, request.email):
        raise HTTPException(409, 'Account already exist')
    try:
        user = db_user.create_user(db, request)
        return user
    except Exception as e:
        return e

@router.post('/login', response_model=Token)
async def login(
    db: Annotated[Session, Depends(get_pg_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = db_user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, 'Invalid email or password')
    access_token = await Auth.encode_access_token(form_data.username)
    refresh_token = await Auth.encode_refresh_token(form_data.username)
    
    content = {'access_token': access_token, 'token_type': 'bearer'}
    response = JSONResponse(content=content)
    response.set_cookie(key="refresh_token", value=refresh_token)
    
    return response

@router.post('/refresh', response_model=Token)
async def refresh_token(refresh_token: Annotated[str, Cookie(min_length=1)]):
    new_access_token, new_refresh_token = await Auth.refresh_token(refresh_token)
    
    content = {'access_token': new_access_token, 'token_type': 'bearer'}
    response = JSONResponse(content=content)
    response.set_cookie(key="refresh_token", value=new_refresh_token)
    
    return response

@router.get("/me", response_model=UserDisplay)
async def user_me(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)]
):
    return current_user