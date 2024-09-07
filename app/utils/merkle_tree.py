import hashlib

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = self.build_tree()

    def build_tree(self):
        leaves = [self.hash(tx.serialize()) for tx in self.transactions]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])
        tree = leaves
        while len(tree) > 1:
            tree = [self.hash(tree[i] + tree[i+1]) for i in range(0, len(tree), 2)]
        return tree

    @staticmethod
    def hash(data):
        return hashlib.sha256(data.encode()).hexdigest()

    def get_root(self):
        return self.tree[0] if self.tree else None

# Update Block class to use Merkle Tree
class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = MerkleTree(transactions).get_root()