# Transaction Input:
#   Contains information for the history of NBCs transferred (previous transactions) and the destination block.
#   It is consisted by PreviousOutputId field, which is the Transaction Output from which the amount of NBCs
#   is originated.

class TransactionInput:
    """
    The transaction input of a noobcash transaction.

    Attributes:
        previous_output_id (int): id of the transaction that the coins come from.
    """

    def __init__(self, previous_output_id):
        """Inits a TransactionInput."""
        self.previous_output_id = previous_output_id

    def toJSON(self):
        return self.previous_output_id

