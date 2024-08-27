import uuid
import time
import copy


class Transaction:
    def __init__(
        self,
        sender_public_key,
        receiver_public_key,
        description,
        items,
        status,
        original_tx_hash,
        amount,
        type,
        id=None,
        time_stamp=None,
        signature="",
    ):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.description = description
        self.items = items
        self.status = status
        self.original_tx_hash = original_tx_hash
        self.amount = amount
        self.type = type
        if id:
            self.id = id
        else:
            self.id = (uuid.uuid1()).hex
        if time_stamp:
            self.timestamp = time_stamp
        else:
            self.timestamp = time.time()
        self.signature = signature

    def to_json(self):
        data = {
            "sender_public_key": self.sender_public_key,
            "receiver_public_key": self.receiver_public_key,
            "description": self.description,
            "items": self.items,
            "status": self.status,
            "original_tx_hash": self.original_tx_hash,
            "amount": self.amount,
            "type": self.type,
            "id": self.id,
            "time_stamp": self.timestamp,
            "signature": self.signature,
        }

        return data

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        transaction_json = copy.deepcopy(self.to_json())
        transaction_json["signature"] = ""

        return transaction_json

    def equals(self, transaction):
        return self.id == transaction.id
