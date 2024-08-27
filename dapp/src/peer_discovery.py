import threading
import time
from message import Message
from utils import Utils


class PeerDiscovery:
    def __init__(self, node):
        self.socket = node

    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()

    def status(self):
        while True:
            print("Current connections: ")

            for peer in self.socket.peers:
                print(str(peer.ip) + ":" + str(peer.port))

            time.sleep(5)

    def discovery(self):
        while True:
            hnd_msg = self.handshake_message()
            self.socket.broadcast(hnd_msg)

            time.sleep(10)

    def handshake(self, node):
        handshake_message = self.handshake_message()
        self.socket.send(node, handshake_message)

    def handle_message(self, message):
        peers_endpoint = message.sender_endpoint
        peers_list = message.data  # Get list of peers from message data

        # Check if peer is not an existing peer
        new_peer = all(not peer.equals(peers_endpoint) for peer in self.socket.peers)

        if new_peer:
            self.socket.peers.append(peers_endpoint)

        for peer in peers_list:
            if not any(p.equals(peer) for p in self.socket.peers) and not peer.equals(
                self.socket.socket_endpoint
            ):
                self.socket.connect_with_node(peer.ip, peer.port)

    def handshake_message(self):
        endpoint = self.socket.socket_endpoint
        peers = self.socket.peers

        data = peers

        message_type = "DISCOVERY"
        message = Message(endpoint, message_type, data)

        encoded_message = Utils.encode(message)

        return encoded_message
