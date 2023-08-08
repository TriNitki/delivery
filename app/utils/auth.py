from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from ..config import settings
from ..db.postgres import db_user
from ..db.database import get_pg_db
from ..schemas.user import UserDisplay

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
hasher = CryptContext(schemes=['bcrypt'])
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM

class Auth():
    async def encode_password(password):
        return hasher.hash(password)
    
    async def verify_password(password, encoded_password):
        return hasher.verify(password, encoded_password)
    
    async def encode_access_token(email):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': email
        }
        
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
    
    async def decode_access_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if payload['scope'] == 'access_token':
                return payload
            raise HTTPException(401, 'Scope for the token is invalid')
        except ExpiredSignatureError:
            raise HTTPException(401, 'Access token expired')
        except JWTError:
            raise HTTPException(401, 'Invalid token')
    
    async def encode_refresh_token(email):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': email
        }
        
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
    
    async def refresh_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                new_access_token = await Auth.encode_access_token(email)
                new_refresh_token = await Auth.encode_refresh_token(email)
                return new_access_token, new_refresh_token
            raise HTTPException(401, 'Scope for the token is invalid')
        except ExpiredSignatureError:
            raise HTTPException(401, 'Refresh token expired')
        except JWTError:
            raise HTTPException(401, 'Invalid token')
    
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_pg_db)
    ):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = await Auth.decode_access_token(token)
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = db_user.get_user_by_email(db, email)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(
        current_user: Annotated[UserDisplay, Depends(get_current_user)]
    ):
        if not current_user.is_active:
            raise HTTPException(400, "Inactive user")
        return current_user