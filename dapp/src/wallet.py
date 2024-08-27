from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from transaction import Transaction
from block import Block
from utils import Utils


class Wallet:
    def __init__(self):
        self.keyPair = RSA.generate(2048)

    def sign(self, data):
        data_hash = Utils.hash(data)
        sign_cypher = PKCS1_v1_5.new(self.keyPair)
        signature = sign_cypher.sign(data_hash)
        return signature.hex()

    @staticmethod
    def signature_valid(data, signature, public_key_string):
        bytes_signature = bytes.fromhex(signature)
        data_hash = Utils.hash(data)
        public_key = RSA.importKey(public_key_string)
        verify_cypher = PKCS1_v1_5.new(public_key)

        return verify_cypher.verify(data_hash, bytes_signature)

    def public_key_to_string(self):
        return self.keyPair.publickey().exportKey("PEM").decode("utf-8")

    def create_transaction(
        self, receiver, description, items, status, original_tx_hash, amount, type
    ):
        transaction = Transaction(
            self.public_key_to_string(),
            receiver,
            description,
            items,
            status,
            original_tx_hash,
            amount,
            type,
        )

        signature = self.sign(transaction.payload())
        transaction.sign(signature)

        return transaction

    def create_block(self, transactions, last_hash, block_index):
        block = Block(transactions, last_hash, self.public_key_to_string(), block_index)

        signature = self.sign(block.payload())
        block.sign(signature)
        return block

    def create_keys_from_file(self, file_path):
        key = ""
        with open(file_path, "r") as key_file:
            key = RSA.importKey(key_file.read())

        self.keyPair = key
