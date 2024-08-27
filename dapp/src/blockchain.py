from block import Block
from utils import Utils
from pos import POS
from account_model import AccountModel


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = AccountModel()
        self.pos = POS()

    def add_block(self, block):
        self.execute_transactions(block.transactions)

        if self.blocks[-1].block_index < block.block_index:
            self.blocks.append(block)

    def to_json(self):
        json_blocks = [block.to_json() for block in self.blocks]
        return {"blocks": json_blocks}

    def last_hash_valid(self, block):
        last_block_hash = Utils.hash(self.blocks[-1].payload()).hexdigest()
        return last_block_hash == block.last_hash

    def block_index_valid(self, block):
        return self.blocks[-1].block_index == block.block_index - 1

    def get_next_forger(self):
        last_hash = Utils.hash(self.blocks[-1].payload()).hexdigest()

        return self.pos.forger(last_hash)

    def transaction_covered(self, transaction):
        if transaction.type == "EXCHANGE":
            return True

        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        return sender_balance >= transaction.amount

    def get_covered_transactions(self, transactions):
        covered_transactions = []

        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                # TODO: find another solution
                print("Error: transaction not covered by the sender")

        return covered_transactions

    def execute_transaction(self, transaction):
        # Handle stake transaction
        if transaction.type == "STAKE":
            # Stake transactions are send from a wallet to
            # the same wallet
            if transaction.sender_public_key == transaction.receiver_public_key:
                self.pos.update(transaction.sender_public_key, transaction.amount)
                # Update the sender token amount after issuing a
                # stake transaction
                self.account_model.update_balance(
                    transaction.sender_public_key, -transaction.amount
                )
        else:
            self.account_model.update_balance(
                transaction.sender_public_key, -transaction.amount
            )

            # Update the receiver's balance
            self.account_model.update_balance(
                transaction.receiver_public_key, transaction.amount
            )

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    def create_block(self, transactions, forger_wallet):
        covered_transactions = self.get_covered_transactions(transactions)

        self.execute_transactions(covered_transactions)

        block = forger_wallet.create_block(
            covered_transactions,
            Utils.hash(self.blocks[-1].payload()).hexdigest(),
            len(self.blocks),
        )

        self.blocks.append(block)

        return block

    def transaction_exists(self, transaction):
        """Check if a transaction exists in the blockchain"""
        for block in self.blocks:
            for tx in block.transactions:
                if transaction.equals(tx):
                    return True

        return False

    def forger_valid(self, block):
        forger_public_key = self.pos.forger(block.last_hash)
        proposed_block_forger = block.forger

        return forger_public_key == proposed_block_forger

    def transaction_valid(self, transactions):
        covered_transactions = self.get_covered_transactions(transactions)

        return len(covered_transactions) == len(transactions)
