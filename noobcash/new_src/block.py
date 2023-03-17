class Block:
    def __init__(self):
        self.previousHash = 1   # Previous plaintext which is now a unique hash digest that 
                                # cannot be reverted to the original plaintext
        self.nonce = 0          # Proof-Of-Work solution
        