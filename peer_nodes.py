from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship
from utility.database import Base


class Node(Base):
    """The class to map the database table peer_nodes in SQLAlchemy"""
    __tablename__ = 'peer_nodes'
    id = Column(Text, primary_key=True, nullable=False)
    wallet_id = relationship("Wallet", back_populates="peer_node_id")

    def __init__(self, node_id):
        self.id = node_id
