from jwt import PyJWTError
from typing import Union, Any
from datetime import datetime, timedelta
from functools import wraps
import jwt
from typing import List
from sqlalchemy.orm import Session
from controllers.usersController import UserController
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, SecurityScopes
from fastapi import Security
from config.database import get_db
from fastapi import Depends, HTTPException, status, Header
from schemas.tokenPayloadSchema import TokenPayload

SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJSYWR1IiwiVXNlcm5hbWUiOiJSYWR1IiwiZXhwIjoxNjc5MzMyNTk4LCJpYXQiOjE2NzkzMzI1OTh9.giz4rJPX-8g-tYidv7MefnoiXGjQXU8ak9Vy5yyjYWk"
REFRESH_SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY3OTMzMjY1OCwiaWF0IjoxNjc5MzMyNjU4fQ.psyLX51s1do3DoksBYsspyVg61LsUZe_S7o6MPaJm7A"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1  # days

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scopes={}
)


def create_access_token(username: Union[str, Any],
                        expires_delta: int = None,
                        key: str = None, permissions: [dict] = None) -> str:
    encode_key = None
    if key == "refresh":
        encode_key = REFRESH_SECRET_KEY
    elif key == "access":
        encode_key = SECRET_KEY
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # give the token the permissions based on the database permissions
    # consensus its permision base are str:str e.g user:read
    scopes = []
    try:
        for item in permissions:
            key = list(item.keys())[0]
            values = item[key]
            # split the values since they come read:update:etc
            individual_permissions = values.split(":")
            for individual_perm in individual_permissions:
                scopes.append(f"{key}:{individual_perm}")
    except:
        print("USER HAS NO PERMS")
    to_encode = {
        "exp": expires_delta,
        "sub": str(username),
        "scopes": scopes
    }
    encoded_jwt = jwt.encode(to_encode, encode_key, ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db: Session = Depends(get_db)):
    credentials_exception2 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials 2",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception3 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials 3",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    token_data = TokenPayload(**payload)
    # return token_data
    try:
        name: str = token_data.sub
        scopes: List[str] = token_data.scopes
        print(f"TOKEN READ SCOPES: {scopes}")
        if name is None:
            raise credentials_exception2
        token_data = name
    except PyJWTError:
        raise credentials_exception3

    user = UserController.get_user(name=token_data, db=db)
    # return user
    if not user:
        raise credentials_exception

    return user


def has_permission(scope_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(data: str = Depends(oauth2_scheme), *args, **kwargs):
            print(data)
            payload = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
            token_data = TokenPayload(**payload)
            print(token_data)
            return func(*args, **kwargs)

        return wrapper

    return decorator

def check_logged_in_user(db: Session = Depends(get_db), data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials 1",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token=data, credentials_exception=credentials_exception, db=db)
