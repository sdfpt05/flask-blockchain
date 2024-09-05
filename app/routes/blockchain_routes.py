from flask import Blueprint, jsonify, request, current_app
from app.services.blockchain_service import BlockchainService

blockchain_bp = Blueprint('blockchain', __name__)
blockchain_service = BlockchainService()

@blockchain_bp.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain_service.get_chain(current_app.blockchain)), 200

@blockchain_bp.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify({'message': 'Missing values'}), 400

    index = blockchain_service.create_transaction(current_app.blockchain, values)
    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201

@blockchain_bp.route('/mine', methods=['GET'])
def mine():
    block = blockchain_service.mine_block(current_app.blockchain)
    if not block:
        return jsonify({'message': 'No transactions to mine'}), 400

    return jsonify({
        'message': "New Block Forged",
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.nonce,
        'previous_hash': block.previous_hash
    }), 200