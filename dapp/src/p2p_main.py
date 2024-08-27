from node import Node
import argparse

if __name__ == "__main__":
    COMMAND_PARSER = argparse.ArgumentParser(description="Blockchain node")

    COMMAND_PARSER.add_argument(
        "--ip",
        metavar="ip",
        type=str,
        required=True,
        help="Host ip",
    )

    COMMAND_PARSER.add_argument(
        "--port",
        metavar="port",
        type=int,
        required=True,
        help="Peer to peer port number",
    )

    COMMAND_PARSER.add_argument(
        "--api-port",
        metavar="api_port",
        type=int,
        required=True,
        help="API port number",
    )

    COMMAND_PARSER.add_argument(
        "--key-path",
        metavar="key_path",
        type=str,
        required=False,
        default=None,
        help="Key path for the genesis node",
    )

    COMMAND_PARSER.add_argument(
        "--load_transactions",
        metavar="load_transactions",
        type=bool,
        required=False,
        default=False,
        help="Key path for the genesis node",
    )

    ARGS = COMMAND_PARSER.parse_args()

    ip = ARGS.ip
    port = ARGS.port
    api_port = ARGS.api_port
    key_path = ARGS.key_path
    load_transactions = ARGS.load_transactions

    node = Node(ip, port, key_path, load_transactions)
    node.start_p2p()
    node.start_api(api_port)
