from collections import OrderedDict
from utility.printable import Printable
from sqlalchemy import Column, Integer, ForeignKey, Text, REAL
from sqlalchemy.orm import relationship
from utility.database import Base
from merkletools import MerkleTools
from time import time


class Transaction(Printable, Base):
    """A transaction which can be added to a block in the blockchain.

    Attributes:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :signature: The signature of the transaction.
        :amount: The amount of coins sent.
    """

    __tablename__ = 'transactions'
    sender = Column(Text, ForeignKey('wallet.public_key'), nullable=False)
    recipient = Column(Text, ForeignKey('wallet.public_key'), nullable=False)
    amount = Column(REAL, nullable=False)
    signature = Column(Text, primary_key=True, nullable=False)
    mined = Column(Integer, nullable=False, default=0)
    block = Column(Integer, ForeignKey('blockchain.index'), nullable=True)
    time = Column(REAL, default=time())

    sender_wallet = relationship("Wallet", foreign_keys=[sender])
    recipient_wallets = relationship("Wallet", foreign_keys=[recipient])
    tx_in_block = relationship("Block", back_populates="tx_in_block")

    def __init__(self, sender, recipient, signature, amount, mined=0,
                 block=None, timed=0):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature
        self.mined = mined
        self.block = block
        self.time = timed

    @classmethod
    def to_ordered_dict(cls, transaction):
        """Converts this transaction into a (hashable) OrderedDict."""
        return OrderedDict([('sender', transaction['sender']),
                            ('recipient', transaction['recipient']),
                            ('amount', transaction['amount'])])

    @staticmethod
    def to_merkle_tree(list_of_transactions):

        merkle_tree = MerkleTools()
        for tx in list_of_transactions:
            print("tx: ", type(tx))
            print(tx)
            if isinstance(tx, Transaction):
                merkle_tree.add_leaf(tx.signature, True)
            else:
                merkle_tree.add_leaf(tx['signature'], True)
        merkle_tree.make_tree()
        return merkle_tree.get_merkle_root()