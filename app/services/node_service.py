class NodeService:
    def register_node(self, blockchain, node):
        blockchain.register_node(node)

    def resolve_conflicts(self, blockchain):
        return blockchain.resolve_conflicts()

    def get_chain(self, blockchain):
        return [vars(block) for block in blockchain.chain]