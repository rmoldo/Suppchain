class AccountModel:
    def __init__(self):
        # Save all the public keys to all the participants
        # in the network
        self.accounts = []
        # Save the public key and the ammount of tokens
        self.balances = {}

    def add_account(self, public_key_string):
        if public_key_string not in self.accounts:
            self.accounts.append(public_key_string)
            self.balances[public_key_string] = 0

    def get_balance(self, public_key_string):
        if public_key_string not in self.accounts:
            self.add_account(public_key_string)
        return self.balances[public_key_string]

    def update_balance(self, public_key_string, ammount):
        if public_key_string not in self.accounts:
            self.add_account(public_key_string)
        self.balances[public_key_string] += ammount
