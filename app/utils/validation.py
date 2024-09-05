from app.utils.crypto import calculate_hash

def is_valid_proof(block, block_hash, difficulty):
    return (block_hash.startswith('0' * difficulty) and
            block_hash == calculate_hash(block))