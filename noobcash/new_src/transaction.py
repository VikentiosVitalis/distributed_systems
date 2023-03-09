from Crypto.PublicKey import RSA
import Crypto


class Transaction:
    def __init__(self, sender, receiver, ammount):
        self.receiver = receiver
        self.sender = sender
        self.ammount = ammount
        self.tid = Crypto.Random.get_random_bytes(128).decode("ISO-8859-1")
        self.signature = None
    
    def sign_transaction(self, privateKey):
        message = self.transaction_id.encode("ISO-8859-1")
        key = RSA.importKey(privateKey.encode("ISO-8859-1"))
        h = Crypto.Hash.SHA256.new(message)
        signer = Crypto.Signature.new(key)
        self.signature = signer.sign(h).decode('ISO-8859-1')

    
    def validate_transaction():
        if self.signature == None: return False
        return True
    

    #  def sign_transaction(self, private_key):
        # https://pycryptodome.readthedocs.io/en/latest/src/cipher/pkcs1_v1_5.html
        """
        Sign transaction with private key
        """
        signature = PKCS1_v1_5.new(private_key).sign(self.transaction_id)
        return signature