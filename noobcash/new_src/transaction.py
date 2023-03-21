from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from new_src.transactions_input import TransactionInput
from new_src.transactions_output import TransactionOutput
import Crypto
import json

# Each transaction contains information for Noobcash Coins transfers from one wallet to another.
# The class contains:

#   sender_address          = Wallet's public key NBCs are originated.
#   receiver_address        = Wallet's public key in which NBCs will be transferred.
#   amount                  = Exact number of NBCs.
#   transaction_id          = A transaction hash/ID is a unique identifier that serves as a proof that
#                           a transaction was validated and added to the blockhain.
#   transaction_inputs      = Contains information for the exchange history of NBCs in each transaction
#                           and it is constituted by the previousOutputId which is the TransactionOutputId
#                           from which the NBCs are originated.
#   transaction_outputs     = Contains a unique ID identifier, the transaction ID which is originated,
#                           the new owner of the NBCs' and the exact number of NBCs transferred.
#
# A transaction can be created by the wallet owner from which NBCs will be transferred.
# Each transaction gets broadcasted in all the blockhain members.
# During the acceptance of a transaction from any node, the validate_transaction function
# is called in order to verify its validity.

class Transaction:
    def __init__(self, sender, receiver, amount, trInputs, amtLeft, tid=None, signature=None):
        self.receiver = receiver     # Address of receiver
        self.sender = sender         # Address of sender
        self.amount = amount         # The amount which will be transferred
        self.inputs = TransactionInput(trInputs)

        if tid != None:
            self.tid = tid           # tid = Transaction ID
        else:
            self.tid = Crypto.Random.get_random_bytes(128)
        
        self.signature = signature
        self.outputSender = TransactionOutput(self.tid, sender, amtLeft)
        self.outputReceiver = TransactionOutput(self.tid, receiver, amount)


    # JavaScript Obejct Notation (JSON) is a lightweight
    # data-interchange format easily understood by humans and
    # typically used in servers and web applications.

    def toJSON(self):
        tr = {
            'receiver': self.receiver,
            'sender':  self.sender,
            'amount':  self.amount,
            'inputs':  self.inputs.toJSON(),
            'outputSender': self.outputSender.__str__(),
            'outputReceiver': self.outputReceiver.__str__(),
            'signature': self.signature.decode('ISO-8859-1'),
            'tid': self.tid.decode('ISO-8859-1')
        }
        #for i in tr.keys():
        #    print(type(tr[i]), i, tr[i])
        string = json.dumps(tr, sort_keys=True)
        return string

    # The verifySignature def or function checks if the transaction is valid.
    # The transaction signature is verified right after its acceptance

    def verifySignature(self):
        if self.signature == None:
            return False
        
        # SHA-256 is a patented cryptographic hash function
        # that outputs a value that is 256 bits long.
        # Load tid to SHA256

        tmp = SHA256.new()
        tmp.update(self.tid)

        # Cipher is an algorithm for encrypting and decrypting data.
        # Cipher for verification

        cipher = PKCS1_v1_5.new(RSA.import_key(self.sender))

        # Verify
        return cipher.verify(tmp, self.signature)

    # The sign_transaction function signs each transaction with wallet's private key
    def sign_transaction(self): 
        return

    # Hashing is the process of transforming any given key or string of
    # characters into another value.
    # In encryption, hashing turns a plaintext into a unique hash digest
    # that cannot be reverted to the original plaintext.
    # Digest/Hash function

    def hashing(self):
        string = self.convert_to_JSON()
        return SHA256.new(string.encode())
