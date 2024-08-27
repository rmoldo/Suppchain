import time
import copy
import sqlite3
import pickle


class Block:
    def __init__(self, transactions, lastHash, forger, block_ind, signature="", timestamp=None):
        self.block_index = block_ind
        self.transactions = transactions
        self.last_hash = lastHash
        self.timestamp = time.time()
        self.forger = forger
        self.signature = signature
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()


        # Initialize SQLite database connection
        conn = sqlite3.connect("db/blockchain.db")
        c = conn.cursor()

        c.execute(
            """CREATE TABLE IF NOT EXISTS blocks
                         (block_index INTEGER PRIMARY KEY,
                          lastHash TEXT,
                          timestamp REAL,
                          forger TEXT,
                          signature TEXT,
                          transactions BLOB)"""
        )

        conn.commit()

    @staticmethod
    def genesis():
        genesis_block = Block([], "", "", 0)
        # Override the timestamp so that when a new node joins the
        # network the same genesis block will be generated
        genesis_block.timestamp = 0

        return genesis_block

    def sign(self, signature):
        self.signature = signature

    def to_json(self):
        json_transactions = [transaction.to_json() for transaction in self.transactions]

        data = {
            "block_index": self.block_index,
            "last_hash": self.last_hash,
            "signature": self.signature,
            "forger": self.forger,
            "time_stamp": self.timestamp,
            "transactions": json_transactions,
        }

        return data

    def payload(self):
        block_json = copy.deepcopy(self.to_json())
        block_json["signature"] = ""

        return block_json

    def save_to_db(self):
        conn = sqlite3.connect("db/blockchain.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO blocks VALUES (?, ?, ?, ?, ?, ?)",
            (
                self.block_index,
                self.last_hash,
                self.timestamp,
                self.forger,
                self.signature,
                pickle.dumps(self.transactions),
            ),
        )

        conn.commit()
