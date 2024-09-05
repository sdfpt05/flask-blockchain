# tests/test_blockchain.py

import pytest
import json
from app import create_app
from app.models.blockchain import Blockchain, Block
from app.utils.crypto import calculate_hash

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def blockchain():
    return Blockchain()

# Blockchain Model Tests

def test_create_blockchain(blockchain):
    assert len(blockchain.chain) == 1
    assert blockchain.chain[0].index == 0
    assert blockchain.chain[0].previous_hash == "0"

def test_create_block(blockchain):
    new_block = Block(1, [], 1234567890, blockchain.last_block.hash)
    assert new_block.index == 1
    assert new_block.timestamp == 1234567890
    assert new_block.previous_hash == blockchain.last_block.hash

def test_add_block(blockchain):
    initial_length = len(blockchain.chain)
    new_block = Block(1, [], 1234567890, blockchain.last_block.hash)
    proof = blockchain.proof_of_work(new_block)
    assert blockchain.add_block(new_block, proof)
    assert len(blockchain.chain) == initial_length + 1

def test_proof_of_work(blockchain):
    last_block = blockchain.last_block
    new_block = Block(last_block.index + 1, [], 1234567890, last_block.hash)
    proof = blockchain.proof_of_work(new_block)
    assert proof.startswith('0' * blockchain.difficulty)

def test_add_transaction(blockchain):
    transaction = {
        'sender': 'sender_address',
        'recipient': 'recipient_address',
        'amount': 5
    }
    index = blockchain.add_transaction(**transaction)
    assert index == blockchain.last_block.index + 1
    assert transaction in blockchain.pending_transactions

def test_mine(blockchain):
    blockchain.add_transaction('sender', 'recipient', 1)
    initial_length = len(blockchain.chain)
    mined_block = blockchain.mine()
    assert mined_block is not None
    assert len(blockchain.chain) == initial_length + 1
    assert len(blockchain.pending_transactions) == 0

def test_is_valid_chain(blockchain):
    # Create a valid chain
    blockchain.add_transaction('sender', 'recipient', 1)
    blockchain.mine()
    
    # Test with the valid chain
    assert blockchain.is_valid_chain(blockchain.chain)
    
    # Tamper with the chain
    blockchain.chain[1].transactions[0]['amount'] = 100
    blockchain.chain[1].hash = calculate_hash(blockchain.chain[1])
    
    # Test with the invalid chain
    assert not blockchain.is_valid_chain(blockchain.chain)

def test_resolve_conflicts(blockchain):
    # Create a longer valid chain
    blockchain2 = Blockchain()
    blockchain2.add_transaction('sender', 'recipient', 1)
    blockchain2.mine()
    blockchain2.add_transaction('sender', 'recipient', 2)
    blockchain2.mine()
    
    # Add the new chain as a node and resolve conflicts
    blockchain.nodes.add('http://testnode.com')
    blockchain.resolve_conflicts = lambda: blockchain2.chain  # Mock the network call
    
    replaced = blockchain.resolve_conflicts()
    assert replaced
    assert len(blockchain.chain) == len(blockchain2.chain)

# API Endpoint Tests

def test_get_chain(client):
    response = client.get('/chain')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the genesis block should be present

def test_new_transaction(client):
    transaction = {
        "sender": "sender_address",
        "recipient": "recipient_address",
        "amount": 5
    }
    response = client.post('/transactions/new', json=transaction)
    assert response.status_code == 201
    assert "Transaction will be added to Block" in response.get_json()["message"]

def test_mine_block(client):
    # Add a transaction first
    transaction = {
        "sender": "sender_address",
        "recipient": "recipient_address",
        "amount": 5
    }
    client.post('/transactions/new', json=transaction)

    # Mine a block
    response = client.get('/mine')
    assert response.status_code == 200
    data = response.get_json()
    assert "New Block Forged" in data["message"]
    assert "transactions" in data
    assert len(data["transactions"]) > 0

def test_register_nodes(client):
    nodes = {
        "nodes": ["http://192.168.0.5:5000", "http://192.168.0.6:5000"]
    }
    response = client.post('/nodes/register', json=nodes)
    assert response.status_code == 201
    data = response.get_json()
    assert "New nodes have been added" in data["message"]
    assert len(data["total_nodes"]) == 2

def test_consensus(client):
    # This test is a bit tricky as it involves network calls
    # For simplicity, we'll just check if the endpoint responds correctly
    response = client.get('/nodes/resolve')
    assert response.status_code == 200
    data = response.get_json()
    assert "chain" in data

def test_invalid_transaction(client):
    transaction = {
        "sender": "sender_address",
        "recipient": "recipient_address",
        # Missing 'amount' field
    }
    response = client.post('/transactions/new', json=transaction)
    assert response.status_code == 400
    assert "Missing values" in response.get_json()["message"]

def test_mine_empty_blockchain(client):
    # Ensure the blockchain is empty (only genesis block)
    client.get('/mine')  # Mine any pending transactions
    
    response = client.get('/mine')
    assert response.status_code == 400
    assert "No transactions to mine" in response.get_json()["message"]

def test_chain_validity_after_mining(client):
    # Add a transaction
    transaction = {
        "sender": "sender_address",
        "recipient": "recipient_address",
        "amount": 5
    }
    client.post('/transactions/new', json=transaction)

    # Mine a block
    client.get('/mine')

    # Get the chain
    response = client.get('/chain')
    chain = response.get_json()

    # Verify the chain
    blockchain = Blockchain()
    assert blockchain.is_valid_chain(chain)

