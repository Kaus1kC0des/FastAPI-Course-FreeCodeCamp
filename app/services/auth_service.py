from typing import Annotated
from datetime import timedelta, datetime
from jose import JWTError, jwt
from pwdlib import PasswordHash
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import Token
import os

SECRET_KEY = os.getenv("SECRET_KEY", "")
ACCESS_TOKEN_EXPIRY_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0))
ALGORITHM = os.getenv("ALGORITHM", "")

password_hash = PasswordHash.recommended()
oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash(password: str):
    return password_hash.hash(password=password)


def verify_password(password: str, original: str):
    return password_hash.verify(password, original)


def create_access_token(data: dict, expires_on: float | int = 0):
    to_encode = data.copy()
    if not expires_on:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
        to_encode.update({"exp": expire})
    token = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=token, token_type="bearer")


def verify_access_token(
    token: str | OAuth2PasswordBearer, credentials_exception: Exception
):
    try:
        out = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = out.get("user_id")
        if not user_id:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


def get_current_user(token: Annotated[OAuth2PasswordBearer, Depends(oauth_schema)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You do not have access to this resource, could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
