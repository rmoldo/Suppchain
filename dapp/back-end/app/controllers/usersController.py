from fastapi import Depends, status, HTTPException, Security
from config.database import get_db
from models.user import User, UserBase, partial
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.hashing import Hashing
from typing import List
from Crypto.PublicKey import RSA


class UserController:
    async def get_allUser(db: AsyncSession):
        result = await db.execute(select(User))
        result = result.scalars().all()
        return result
        # return result.scalars().all()

    async def get_user(name: str, db: AsyncSession = Depends(get_db)):
        statement = select(User).where(User.name == name)
        result = await db.execute(statement)
        data = result.scalar_one_or_none()
        return data

    async def get_user_by_id(id: int, db: AsyncSession = Depends(get_db)):
        statement = select(User).where(User.id == id)
        result = await db.execute(statement)
        data = result.scalar_one_or_none()
        return data

    async def create_user(user: UserBase, db: AsyncSession = Depends(get_db)):
        db_user = User(**user.dict())
        #generate the key
        key = RSA.generate(2048)
        db_user.key_pairs= key.exportKey(format="PEM")
        # hash the password
        db_user.password = Hashing.bcrypt(user.password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def update_user(userid: int, user: partial(UserBase), db: AsyncSession):
        statement = select(User).where(User.id == userid)
        result = await db.execute(statement)
        db_user = result.scalar_one_or_none()

        incoming_user = user.dict(exclude_unset=True)
        for k, v in incoming_user.items():
            # set the atribute k of the db_user object to value v
            setattr(db_user, k, v)
        # db_user = jsonable_encoder(merge(db_user.dict(), incoming_user))
        print(db_user)

        await db.commit()
        return db_user

    async def deleteUser(userid: int, db: AsyncSession):
        statement = select(User).where(User.id == userid)
        result = await db.execute(statement)
        db_user = result.scalar_one_or_none()
        await db.delete(db_user)
        await db.commit()
