from utils import Utils


class Lot:
    def __init__(self, public_key, number_of_lots, last_hash):
        self.public_key = str(public_key)
        self.number_of_lots = number_of_lots
        self.last_hash = last_hash

    def hash_lot(self):
        """Hash the lot"""
        data_hash = self.public_key + self.last_hash

        for _ in range(self.number_of_lots):
            data_hash = Utils.hash(data_hash).hexdigest()

        return data_hash
