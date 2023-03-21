# Transaction Output:
#   It is consisted by a unique identifier of the transactions (tid), 
#   the id of transaction which it is originated, 
#   the new owner of the NBCs (recipient),
#   the amount transferred.

class TransactionOutput:
    """
    A transaction output of a noobcash transaction.

    Attributes:
        transaction_id (int): id of the transaction.
        recipient (int): the recipient of the transaction.
        amount (int): the amount of nbcs to be transfered.
        unspent (boolean): false if this output has been used as input in a transaction.
    """

    def __init__(self, tid, receiver, amount):
        """Inits a TransactionOutput."""
        self.tid = tid
        self.receiver = receiver
        self.amount = amount
        self.unspent = True

    def fromdict(self, output_dict):
        self.tid = output_dict['tid']
        self.receiver = output_dict['receiver']
        self.amount = output_dict['amount']
        self.unspent = True

    def __str__(self):
        """Returns a string as a representation of a TransactionOutput object"""
        return str(self.__dict__)

