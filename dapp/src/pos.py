from lot import Lot
from utils import Utils


class POS:
    def __init__(self):
        self.stakers = {}
        self.set_genesis_node_stake()

    def update(self, public_key_string, stake):
        """Update the amound of tokens staked for a node"""

        if public_key_string in self.stakers.keys():
            self.stakers[public_key_string] += stake
        else:
            self.stakers[public_key_string] = stake

    def get_stake(self, public_key_string):
        """Get stake coresponding to the node's public key"""

        if public_key_string in self.stakers.keys():
            return self.stakers[public_key_string]
        else:
            return None

    def lot_validators(self, seed):
        """Generate all the lots for a specific validator"""

        lots = []

        for validator_key in self.stakers.keys():
            for stake in range(self.get_stake(validator_key)):
                lots.append(Lot(validator_key, stake + 1, seed))

        return lots

    def lot_winner(self, lots, seed):
        """Pick a winner based on the shortest offset from seed"""

        winner_lot = None
        offset = None

        start_hash_int = int(
            Utils.hash(seed).hexdigest(), 16
        )  # get the uint16_t representation of the seed hash

        for lot in lots:
            lot_hash_int = int(lot.hash_lot(), 16)

            off = abs(lot_hash_int - start_hash_int)

            if offset is None or off < offset:
                offset = off
                winner = lot

        return winner

    def forger(self, last_hash):
        """Get the new forgers public key"""

        # Generate all the lots based on the last block hash
        lots = self.lot_validators(last_hash)

        lot_winner = self.lot_winner(lots, last_hash)

        return lot_winner.public_key

    def set_genesis_node_stake(self):
        """Ugly solution but I do not care"""
        genesis_public_key = open("keys/genesis_pub.pem", "r").read()
        self.stakers[genesis_public_key] = 1
