from transaction_pool import TransactionPool
from blockchain import Blockchain
from wallet import Wallet
from network_socket import NetworkSocket
from message import Message
from utils import Utils
from api import API
from block import Block
import os
import json
import copy
from transaction import Transaction


class Node:
    def __init__(self, host_ip, port, key_path=None, load_transactions=False):
        self.transaction_pool = TransactionPool()
        # We need a wallet so that the node can sign blocks
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        self.p2p = None
        self.host_ip = host_ip
        self.port = port
        self.load_transactions = load_transactions
        self.static_transactions = []
        if key_path is not None:
            self.wallet.create_keys_from_file(key_path)

    #
    def load_transactions_from_json(self, json_data):
        transactions = []
        for transaction in json_data["transactions"]:
            transaction_object = Transaction(
                sender_public_key=transaction["sender_public_key"],
                receiver_public_key=transaction["receiver_public_key"],
                description=transaction["description"],
                items=transaction["items"],
                status=transaction["status"],
                original_tx_hash=transaction["original_tx_hash"],
                amount=transaction["amount"],
                type=transaction["type"],
                id=transaction["id"],
                time_stamp=transaction["time_stamp"],
                signature=transaction["signature"],
            )
            transactions.append(transaction_object)
        return transactions

    def load_data(self, port):
        path = f"./data/{port}.json"
        if os.path.isfile(path) and os.access(path, os.R_OK):
            # checks if file exists
            print(f"{port}.json exits and will loading data from it")
            with open(path, "r") as openfile:
                local_node_data = json.load(openfile)
                # load transactions into the node
                transactions = self.load_transactions_from_json(local_node_data)
                self.static_transactions = transactions
            # load blockhain
            for block in local_node_data["blockchains"]:
                print(block)
                print(type(block))
                transactions = self.load_transactions_from_json(block)
                block_object = Block(
                    block_ind=block["block_index"],
                    lastHash=block["last_hash"],
                    signature=block["signature"],
                    forger=block["forger"],
                    timestamp=block["time_stamp"],
                    transactions=transactions,
                )
                self.blockchain.add_block(block_object)
                # self.manage_transaction(transaction_object)
        else:
            print(f"{port}.json does not exist, can not load data")

    def start_p2p(self):
        self.p2p = NetworkSocket(self.host_ip, self.port)
        self.p2p.start_network_socket(self)
        print(self.load_transactions)
        if self.load_transactions:
            print("LOADING TRANSACTIONS FROM JSON")
            self.load_data(port=self.port)

    def start_api(self, api_port):
        self.api = API()
        self.api.inject_node(self)
        self.api.start(api_port)

    def add_value_to_local_json(self, data, key):
        if key == "blockchains":
            print("BLOCKHAIN KEY")
        data_json = data.to_json()
        path = f"./data/{self.port}.json"
        if os.path.isfile(path) and os.access(path, os.R_OK):
            # checks if file exists
            with open(path, "r") as openfile:
                local_node_data = json.load(openfile)
            # only add the value if the transaction does not exist already
            if key == "transactions":
                transaction_exits = False
                for transaction in local_node_data["transactions"]:
                    if transaction["id"] == data_json["id"]:
                        transaction_exits = True
                        break
                # add the transaction if it's not there already
                if not transaction_exits:
                    local_node_data["transactions"].append(data_json)
            if key == "blockchains":
                local_node_data["blockchains"].append(data_json)
            with open(path, "w") as outfile:
                outfile.write(json.dumps(local_node_data, indent=4))
        else:
            data = {
                "transactions": [],
                "blockchains": [],
            }
            data[key].append(data_json)
            with open(path, "w") as outfile:
                outfile.write(json.dumps(data, indent=4))

    def forge(self):
        forger = self.blockchain.get_next_forger()

        if forger == self.wallet.public_key_to_string():
            print("I am the next forger")
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet
            )

            # Update the transaction pool by removing the transactions
            # from the local instance of the transaction pool
            self.transaction_pool.remove_from_pool(block.transactions)
            self.add_value_to_local_json(block, "blockchains")

            # Broadcast the new block
            message = Message(self.p2p.socket_endpoint, "BLOCK", block)
            self.p2p.broadcast(Utils.encode(message))
        else:
            print("I am not the next forger")

    def manage_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        public_key = transaction.sender_public_key
        # print(data)
        # print(type(data))
        print(signature)
        print(public_key)
        is_valid = self.wallet.signature_valid(data, signature, public_key)
        is_valid = True
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        is_transaction_in_blockchain = self.blockchain.transaction_exists(transaction)
        print("GOT HERE!")
        print(transaction_exists)
        print(is_valid)
        print(is_transaction_in_blockchain)
        if not transaction_exists and is_valid and not is_transaction_in_blockchain:
            print("GOT HERE 2 !!!!!")
            self.transaction_pool.add_transaction(transaction)
            self.add_value_to_local_json(transaction, "transactions")
            self.static_transactions.append(transaction)
            print("SUCEEED")
            message = Message(self.p2p.socket_endpoint, "TRANSACTION", transaction)
            self.p2p.broadcast(Utils.encode(message))
            should_select_new_forger = self.transaction_pool.should_select_new_forger()

            if should_select_new_forger:
                self.forge()

    def manage_block(self, block):
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature

        is_block_index_valid = self.blockchain.block_index_valid(block)
        last_hash_valid = self.blockchain.last_hash_valid(block)
        forger_valid = self.blockchain.forger_valid(block)
        transaction_valid = self.blockchain.transaction_valid(block.transactions)
        signature_valid = Wallet.signature_valid(block_hash, signature, forger)

        if not is_block_index_valid:
            self.request_chain()

        if (
            last_hash_valid
            and forger_valid
            and transaction_valid
            and signature_valid
            and is_block_index_valid
        ):
            self.blockchain.add_block(block)
            self.add_value_to_local_json(block, "blockchains")
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socket_endpoint, "BLOCK", block)
            self.p2p.broadcast(Utils.encode(message))

    def request_chain(self):
        message = Message(self.p2p.socket_endpoint, "CHAINREQUEST", None)
        self.p2p.broadcast(Utils.encode(message))

    def handle_blockchain_request(self, requester_node):
        message = Message(self.p2p.socket_endpoint, "BLOCKCHAIN", self.blockchain)
        self.p2p.send(requester_node, Utils.encode(message))

    def manage_blockchain(self, blockchain):
        local_chain = copy.deepcopy(self.blockchain)

        local_chain_len = len(local_chain.blocks)

        received_chain_len = len(blockchain.blocks)

        if local_chain_len < received_chain_len:
            for index, block in enumerate(blockchain.blocks):
                if index >= local_chain_len:
                    local_chain.add_block(block)
                    self.add_value_to_local_json(block, "blockchains")
                    self.transaction_pool.remove_from_pool(block.transactions)

            self.blockchain = local_chain
