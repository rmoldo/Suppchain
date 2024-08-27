from typing import List, Optional, Type
from sqlmodel import Field, SQLModel, Relationship, Column, JSON
import time
import uuid
from pydantic import BaseModel, create_model
from functools import lru_cache
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from config.utils import Utils
import copy


class TransactionBase(SQLModel):
    reciver_user_id: int = Field(default = 0, exclude= True)
    description: str
    amount: int
    items: str
    status: str
    original_tx_hash: str
    type: str

class Transaction(TransactionBase, table=False):
    id :str = Field(default= (uuid.uuid1()).hex , exclude= False)
    time_stamp: str = Field(default= time.time(), exclude= False)
    signature:str = Field(default= "", exclude= False)
    sender_public_key: str = Field(default= None, exclude= False)
    receiver_public_key: str = Field(default=None, exclude=False)

    def to_json(self):
        data = {
            "sender_public_key": self.sender_public_key,
            "receiver_public_key": self.receiver_public_key,
            "description": self.description,
            "amount": self.amount,
            "type": self.type,
            "id": self.id,
            "time_stamp": self.time_stamp,
            "signature": self.signature,
            "items": self.items,
            "status": self.status,
            "original_tx_hash": self.original_tx_hash
        }

        return data

    def payload(self):
        transaction_json = copy.deepcopy(self.to_json())
        transaction_json["signature"] = ""

        return transaction_json

