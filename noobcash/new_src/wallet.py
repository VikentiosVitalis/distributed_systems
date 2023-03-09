from Crypto.PublicKey import RSA


class Wallet:
    def __init__():
        # Generate key
        key = RSA.generate(1024)
        # Get data from keys
        self._privateKey = key.exportKey().decode('ISO-8859-1')
        # Also user's address
        self.publicKey = key.publickey().exportKey().decode('ISO-8859-1')
        # Transaction list
        # self.transactions = []
    def get_addr():
        return self.publicKey
    def sign(message):
        # Sign message = sign message
        return message




