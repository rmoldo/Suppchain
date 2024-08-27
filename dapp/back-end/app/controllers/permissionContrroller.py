from fastapi import Depends, status, HTTPException
from config.database import get_db
from models.permissions import Permission, PermissionBase
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class PermissionController:
    async def get_allPermissions(db: AsyncSession):
        result = await db.execute(select(Permission))
        result = result.scalars().all()
        return result

    async def get_permission(acl_group: str, db: AsyncSession = Depends(get_db)):
        statement = select(Permission).where(Permission.acl_group == acl_group)
        result = await db.execute(statement)
        data = result.scalar_one_or_none()
        return data


    async def create_permission(permission: PermissionBase, db: AsyncSession = Depends(get_db)):
        db_permission = Permission(**permission.dict())
        print(permission.dict())
        # hash the password
        db.add(db_permission)
        await db.commit()
        await db.refresh(db_permission)
        return db_permission

    # async def update_user(userid: int, user: partial(UserBase), db: AsyncSession):
    #     statement = select(User).where(User.id == userid)
    #     result = await db.execute(statement)
    #     db_user = result.scalar_one_or_none()
    #
    #     incoming_user = user.dict(exclude_unset=True)
    #     for k, v in incoming_user.items():
    #         # set the atribute k of the db_user object to value v
    #         setattr(db_user, k, v)
    #     # db_user = jsonable_encoder(merge(db_user.dict(), incoming_user))
    #     print(db_user)
    #
    #     await db.commit()
    #     return db_user

    async def deletePermission(id: int, db: AsyncSession):
        statement = select(Permission).where(Permission.id == id)
        result = await db.execute(statement)
        db_user = result.scalar_one_or_none()
        await db.delete(db_user)
        await db.commit()
