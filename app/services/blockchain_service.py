class BlockchainService:
    def get_chain(self, blockchain):
        return [vars(block) for block in blockchain.chain]

    def create_transaction(self, blockchain, transaction):
        return blockchain.add_transaction(
            transaction['sender'],
            transaction['recipient'],
            transaction['amount']
        )

    def mine_block(self, blockchain):
        return blockchain.mine()