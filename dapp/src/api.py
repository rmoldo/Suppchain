from flask_classful import FlaskView, route
from flask import Flask, request, jsonify
from utils import Utils
from flask_cors import CORS, cross_origin
import json
from transaction import Transaction
node = None


class API(FlaskView):
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
    def start(self, api_port):
        API.register(self.app, route_base="/")
        self.app.run(host="localhost", port=api_port)

    def inject_node(self, chain_node):
        global node
        node = chain_node

    @route("/blockchain", methods=["GET"])
    def blockchain(self):
        return node.blockchain.to_json(), 200

    @route("/transactions", methods=["GET"])
    def transactions(self):
        txs = {}
        for index, tx in enumerate(node.static_transactions):
            txs[index] = tx.to_json()

        return jsonify(txs), 200

    @route("/transaction", methods=["POST"])
    def transaction(self):
        values = request.get_json()
        print(f"RECEIVED TRANSACTION {values}")
        if "transaction" not in values:
            return "No transaction", 400

        # tx = Utils.decode(values["transaction"])

        transaction = Transaction(**values["transaction"])
        print(f"NEW TRANSACTIOn {transaction}")
        print(f"NEW TRANSACTIOn {json.dumps(transaction.to_json(), indent=4)}")
        node.manage_transaction(transaction)

        response = {"message": "Transaction has been received"}
        return jsonify(response), 201
