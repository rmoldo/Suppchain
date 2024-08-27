from p2pnetwork.node import Node
from peer_discovery import PeerDiscovery
from socket_endpoint import SocketEndpoint
from utils import Utils
import json


class NetworkSocket(Node):
    def __init__(self, ip, port):
        super(NetworkSocket, self).__init__(ip, port, None)
        self.peers = []
        self.peer_discovery = PeerDiscovery(self)
        self.socket_endpoint = SocketEndpoint(ip, port)

    def start_network_socket(self, node):
        self.node = node
        self.start()
        self.peer_discovery.start()
        self.connect_to_first_node()

    def inbound_node_connected(self, connected_node):
        self.peer_discovery.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        self.peer_discovery.handshake(connected_node)

    def node_message(self, connected_node, message):
        # Get the original message object
        original_message = Utils.decode(json.dumps(message))

        if original_message.message_type == "DISCOVERY":
            self.peer_discovery.handle_message(original_message)
        elif original_message.message_type == "TRANSACTION":
            tx = original_message.data
            self.node.manage_transaction(tx)
        elif original_message.message_type == "BLOCK":
            block = original_message.data
            self.node.manage_block(block)
        elif original_message.message_type == "CHAINREQUEST":
            self.node.handle_blockchain_request(connected_node)
        elif original_message.message_type == "BLOCKCHAIN":
            blockchain = original_message.data
            self.node.manage_blockchain(blockchain)

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)

    def connect_to_first_node(self):
        if self.socket_endpoint.port != 10001:
            self.connect_with_node("localhost", 10001)
