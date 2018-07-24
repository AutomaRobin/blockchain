import hashlib as hl
import json
from block import Block


def hash_string_256(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    index = block['index']
    previous_hash = block['previous_hash']
    hash_of_txs = block['hash_of_txs']
    proof = block['proof']
    timestamp = block['timestamp']

    blocked = Block(index, previous_hash, hash_of_txs, proof, timestamp)
    hashable_block = blocked.block_to_ordered_dict()
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
