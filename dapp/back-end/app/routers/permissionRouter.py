from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models.permissions import Permission, PermissionBase
from typing import List
from controllers.permissionContrroller import PermissionController
from config.token import check_logged_in_user
from typing import Annotated
import os

router = APIRouter(prefix="/permission", tags=["Permissions"])


@router.get("/", response_model= List[Permission])
async def getAllPermissions(db: AsyncSession = Depends(get_db)):
    return await PermissionController.get_allPermissions(db=db)


@router.post("/", response_model=Permission)
async def createPermission(permission: PermissionBase, db: AsyncSession = Depends(get_db)):
    return await PermissionController.create_permission(permission, db)

@router.get("/{acl_group}", response_model= Permission)
async def getPermission(acl_group: str, db: AsyncSession = Depends(get_db)):
    return await PermissionController.get_permission(acl_group=acl_group, db=db)

# @router.patch("/{acl_group}", response_model=User)
# async def updateUser(userid: int, user: partial(UserBase), db: AsyncSession = Depends(get_db)):
#     return await UserController.update_user(userid=userid, user=user, db=db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: int, db: AsyncSession = Depends(get_db)):
    return await PermissionController.deletePermission(id=id, db=db)
