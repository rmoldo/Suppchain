import json

from fastapi import Depends, status, HTTPException, Security
from config.database import get_db
from models.user import User, UserBase, partial
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.hashing import Hashing
from typing import List
from Crypto.PublicKey import RSA
from models.transaction import Transaction, TransactionBase
from controllers.usersController import UserController
from config.token import check_logged_in_user, has_permission
from config.utils import Utils
import requests
import time
import uuid
import json

class TransactionController:

    async def create_transaction(transaction: TransactionBase, current_user: User, db: AsyncSession):

        transaction_output = Transaction(**transaction.dict())
        transaction_output.time_stamp = time.time()
        transaction_output.id = (uuid.uuid1()).hex

        transaction_output.reciver_user_id = transaction.reciver_user_id

        #generate the key
        # print(current_user)
        # current_user.key_pairs = RSA.importKey(current_user.key_pairs)
        transaction_output.sender_public_key =  User.public_key_to_string(current_user.key_pairs)
        # print("HEREEEE")
        # print(transaction.reciver_user_id)
        reciver_user = await UserController.get_user_by_id(transaction_output.reciver_user_id, db)
        # print(reciver_user)
        # reciver_user.key_pairs = RSA.importKey(reciver_user.key_pairs)
        transaction_output.receiver_public_key = User.public_key_to_string(reciver_user.key_pairs)
        # TO DO: SIGN THE TRANSACTION

        signature = current_user.sign(transaction_output.payload(), RSA.importKey(current_user.key_pairs))
        print(signature)
        print(transaction_output.sender_public_key)
        valid_signature = current_user.signature_valid(transaction_output.payload(),signature,transaction_output.sender_public_key)
        print(f"VALID SIGNATURE: {valid_signature}")
        transaction_output.signature = signature

        return transaction_output

