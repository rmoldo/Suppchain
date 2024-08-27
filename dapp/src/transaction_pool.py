class TransactionPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def transaction_exists(self, transaction):
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):
                return True
        return False

    def remove_from_pool(self, transactions):
        self.transactions = [
            transaction
            for transaction in self.transactions
            if not any(transaction.equals(tx) for tx in transactions)
        ]

    def should_select_new_forger(self):
        """Check if threshold of a transaction in the tp is
        reached and signal the creation of a new block"""

        return len(self.transactions) >= 1
