import json

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models.user import User, UserBase, partial
from controllers.usersController import UserController
from typing import Annotated, List
from config.token import check_logged_in_user, has_permission
from models.user import User, UserBase, partial
from models.transaction import TransactionBase, Transaction
from controllers.transactionController import TransactionController
import os

router = APIRouter(prefix="/transaction", tags=["Transaction"])

@router.post("/", response_model=Transaction)
async def create_transaction(transaction: TransactionBase, current_user: User = Depends(check_logged_in_user), db: AsyncSession = Depends(get_db)):
    user = await current_user
    transaction = await TransactionController.create_transaction(transaction,user, db)
    return transaction




