from app.models.blockchain import Block, Blockchain
from app import db

class BlockchainService:
    def __init__(self):
        self.blockchain = Blockchain()
        self.nodes = set()

    def get_chain(self):
        chain = Block.query.order_by(Block.index).all()
        return [block.__dict__ for block in chain]

    def get_last_block(self):
        return self.blockchain.last_block

    def mine(self):
        return self.blockchain.mine()

    def add_transaction(self, transaction):
        return self.blockchain.add_new_transaction(transaction)

    def register_node(self, address):
        self.nodes.add(address)

    def resolve_conflicts(self):
        # Implement the consensus algorithm
        # This is a placeholder and should be implemented properly
        return False