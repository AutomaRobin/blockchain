from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii
from sqlalchemy import Column, Text, text
from utility.database import Base, Session


class Wallet(Base):
    """Creates, loads and holds private and public keys. Manages transaction
    signing and verification."""

    __tablename__ = 'wallet'
    public_key = Column(Text, primary_key=True, nullable=False)
    node_id = Column(Text, nullable=False)

    def __init__(self, node_id, private_key=None, public_key=None):
        self.private_key = private_key
        self.public_key = public_key
        self.node_id = node_id

    def create_keys(self):
        """Create a new pair of private and public keys."""
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        """Saves the keys to a file (wallet.txt)."""
        if self.public_key is not None and self.private_key is not None:
            try:
                with open('wallet-{}.txt'.format(self.node_id), mode='w') as f:
                    f.write(self.private_key)
                session = Session()
                wallet = Wallet(node_id=self.node_id, public_key=self.public_key)
                session.add(wallet)
                session.commit()
                session.close()
                return True
            except (IOError, IndexError):
                print('Saving wallet failed...')
                return False

    def load_keys(self, private_key):
        """Loads the wallet based on the private key."""

        # prepare the private_key input to be transformed to the public_key
        hex_to_pem = binascii.unhexlify(''.join(private_key))
        pem_key = b'%s' % hex_to_pem
        kep_priv = RSA.importKey(pem_key)
        candidate_key = kep_priv.publickey()
        query_key = binascii.hexlify(candidate_key.exportKey(format='DER')).decode('ascii')

        # Pass the candidate key for the
        # SQL query and search database for the public_key
        session = Session()
        public_key = session.query(Wallet.public_key)\
            .filter(text('public_key == :query_key')).params(query_key=query_key).one()
        session.close()
        if not public_key:
            return False

        if public_key:
            self.public_key = ''.join(public_key)
            self.private_key = private_key
            return True

    @staticmethod
    def generate_keys():
        """Generate a new pair of private and public key."""
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (
            binascii
            .hexlify(private_key.exportKey(format='DER'))
            .decode('ascii'),
            binascii
            .hexlify(public_key.exportKey(format='DER'))
            .decode('ascii')
        )

    def sign_transaction(self, sender, recipient, amount):
        """Sign a transaction and return the signature.

        Arguments:
            :sender: The sender of the transaction.
            :recipient: The recipient of the transaction.
            :amount: The amount of the transaction.
        """
        signer = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) +
                        str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        """Verify the signature of a transaction.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        print("this is the transaction: ", transaction)
        dict_tx = transaction.__dict__
        del dict_tx['mined']
        del dict_tx['block']
        print(dict_tx['sender'])

        public_key = RSA.importKey(binascii.unhexlify(dict_tx['sender']))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(dict_tx['sender']) + str(dict_tx['recipient']) +
                        str(dict_tx['amount'])).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(dict_tx['signature']))
