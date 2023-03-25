from src.transaction import Transaction
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
        self.transactions = [tr.toJSON() for tr in transactions]
        self.nonce = nonce                      # Proof-Of-Work solution
        self.previous_hash = previous_hash      # Previous plaintext which is now a unique hash digest that
                                                # cannot be reverted to the original plaintext
        self.goal = '0'*DIFFICULTY
        self.timestamp = timestamp
        self.current_hash = '-1'

    def set(self, inp): # Init from json file
        self.index = int(inp['index'])
        self.transactions = [i for i in inp['transactions']]
        self.nonce = int(inp['nonce'])
        self.previous_hash = inp['previous_hash']
        self.current_hash = inp['current_hash']
        self.timestamp = float(inp['timestamp'])

    def convert_block(self):
        res = json.dumps(dict(index = self.index, timestamp = self.timestamp.__str__(), 
            transactions = self.transactions, nonce = self.nonce, 
            current_hash = self.current_hash, previous_hash=self.previous_hash), sort_keys=True)
        return (res)
    
    # Hashing is the process of transforming any given key or string of
    # characters into another value.
    # In encryption, hashing turns a plaintext into a unique hash digest
    # that cannot be reverted to the original plaintext.
    # Digest/Hash function

    def hashing(self):
        x = json.loads(self.convert_block())
        del x['current_hash']
        res = hasher.sha256(json.dumps(x).encode()).hexdigest()
        return res

    def mine_block(self, temp):
        while self.hashing()[:DIFFICULTY] != self.goal:
            if temp.isSet():
                return 0
            self.nonce += 1
        self.current_hash = self.hashing()
        return
