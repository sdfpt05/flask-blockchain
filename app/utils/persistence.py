import pickle

def save_blockchain(blockchain, filename='blockchain.dat'):
    with open(filename, 'wb') as f:
        pickle.dump(blockchain, f)

def load_blockchain(filename='blockchain.dat'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

# Update Blockchain class
class Blockchain:
    @classmethod
    def load_or_create(cls):
        blockchain = load_blockchain()
        if blockchain is None:
            return cls()
        return blockchain

    def save(self):
        save_blockchain(self)