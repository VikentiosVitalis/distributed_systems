from new_src.transaction import Transaction
import hashlib as hasher
import time
import json
DIFFICULTY = 4

# Noobcash Block:
#
#   index:          Number of Block (1,2,3...)
#   timestamp:      Time of block creation
#   transactions:   List of a transactions contained in a Block 
#   nonce:          Proof-Of-Work' solution
#   current_hash:   Current Block's plaintext which is now a unique hash digest that cannot be reverted to original plaintext
#   previous_hash:  Previous Block's hash digest
#
# The space of each block for transactions is limited by the constant capacity.

class Block:

    def __init__(self, index, transactions, nonce, previous_hash, timestamp=time.time()):
        # Blocks's info
        self.index = index
        self.transactions = transactions
        self.nonce = nonce                      # Proof-Of-Work solution
        self.previous_hash = previous_hash      # Previous plaintext which is now a unique hash digest that
                                                # cannot be reverted to the original plaintext
        self.timestamp = timestamp
        self.current_hash = -1


    def insertdif(self, dif):
        self.dif = dif

    def convert_block(self):
        res = json.dumps(dict(index = self.index, timestamp = self.timestamp.__str__(), transactions = self.transactions.toJSON(),nonce = self.nonce, current_hash = self.current_hash,previous_hash=self.previous_hash ), sort_keys=True)
        return (res)

    # =================== Mining Process ================= #

    def hashing(self):
        '''
        :return: current block's hash
        '''
        x = json.loads(self.convert_block())
        del x['current_hash']
        res = hasher.sha256(self.convert_block().encode()).hexdigest()
        return res

    def mine_block(self, temp):
        while self.hashing()[:DIFFICULTY] == '0' * DIFFICULTY is False and not temp.isSet():
            self.nonce += 1
        self.current_hash = self.hashing()
        return self