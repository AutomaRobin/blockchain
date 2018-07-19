from collections import OrderedDict
from utility.printable import Printable
from sqlalchemy import Column, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from utility.database import Base


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
    amount = Column(Float, nullable=False)
    signature = Column(Text, primary_key=True, nullable=False)
    mined = Column(Integer, nullable=False)
    block = Column(Integer, ForeignKey('blockchain.index'), nullable=True)
    time = Column(Float, nullable=False)

    sender_wallet = relationship("Wallet", foreign_keys=[sender])
    recipient_wallets = relationship("Wallet", foreign_keys=[recipient])
    tx_in_block = relationship("Block", back_populates="tx_in_block")

    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        """Converts this transaction into a (hashable) OrderedDict."""
        return OrderedDict([('sender', self.sender),
                            ('recipient', self.recipient),
                            ('amount', self.amount)])

