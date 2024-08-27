from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from config.hashing import Hashing
from config.token import create_access_token
from models.user import User
from models.permissions import Permission


async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    statement = select(User).where(User.name == request.username)
    result = await db.execute(statement)
    user: User = result.scalar()

    statement = select(Permission).where(Permission.id == user.acl_group)
    result = await db.execute(statement)
    permission: Permission = result.scalar()
    print(permission)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not Hashing.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password"
        )

    response = {
        "access_token": create_access_token(user.name, key="access", permissions=permission.permissions),
        "refresh_token": create_access_token(user.name, key="refresh", permissions=permission.permissions),
        "username": user.name
    }

    return response
