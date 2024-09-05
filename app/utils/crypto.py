import hashlib
import json

def calculate_hash(block):
    block_string = json.dumps(vars(block), sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()
