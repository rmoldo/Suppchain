from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models.user import User, UserBase, partial
from controllers.usersController import UserController
from typing import Annotated, List
from config.token import check_logged_in_user, has_permission

import os

router = APIRouter(prefix="/users", tags=["Users"])




# @router.get("/", response_model=list[User])
@router.get("/", response_model= List[User])
async def getAllUser(db: AsyncSession = Depends(get_db)):
    return await UserController.get_allUser(db=db)


@router.post("/", response_model=User)
async def createUser(user: UserBase, db: AsyncSession = Depends(get_db)):
    return await UserController.create_user(user, db)


@router.get("/me")
async def getMe(current_user: User = Depends(check_logged_in_user)):
    return await current_user


@router.patch("/{userid}", response_model=User)
async def updateUser(userid: int, user: partial(UserBase), db: AsyncSession = Depends(get_db)):
    return await UserController.update_user(userid=userid, user=user, db=db)


@router.delete("/{userid}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(userid: int, db: AsyncSession = Depends(get_db)):
    return await UserController.deleteUser(userid=userid, db=db)



