from wallet import Wallet
from transaction_pool import TransactionPool
from blockchain import Blockchain
from utils import Utils
import pprint


if __name__ == "__main__":
    blockchain = Blockchain()
    pool = TransactionPool()

    alice_wallet = Wallet()
    bob_wallet = Wallet()
    exchange_wallet = Wallet()
    forger = Wallet()

    # Exchange transaction. Alice will have 6 tokens
    exchange_transaction = exchange_wallet.create_transaction(
        alice_wallet.public_key_to_string(), "Cereale ale ale", 10, "EXCHANGE"
    )

    if not pool.transaction_exists(exchange_transaction):
        pool.add_transaction(exchange_transaction)

    covered_transactions = blockchain.get_covered_transactions(pool.transactions)

    last_hash = Utils.hash(blockchain.blocks[-1].payload()).hexdigest()
    block_index = blockchain.blocks[-1].block_index + 1

    block_one = forger.create_block(covered_transactions, last_hash, block_index)

    blockchain.add_block(block_one)
    pool.remove_from_pool(block_one.transactions)

    # Alice will send 5 tokens to alice
    transaction = alice_wallet.create_transaction(
        bob_wallet.public_key_to_string(), "Bere bere bere", 8, "TRANSFER"
    )

    if not pool.transaction_exists(transaction):
        pool.add_transaction(transaction)

    covered_transactions = blockchain.get_covered_transactions(pool.transactions)

    last_hash = Utils.hash(blockchain.blocks[-1].payload()).hexdigest()

    block_index = blockchain.blocks[-1].block_index + 1

    block_two = forger.create_block(covered_transactions, last_hash, block_index)

    blockchain.add_block(block_two)

    pool.remove_from_pool(block_two.transactions)

    pprint.pprint(blockchain.to_json())
