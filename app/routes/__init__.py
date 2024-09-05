from flask import Blueprint, jsonify, request, current_app
from app.models.models import Block, Blockchain
from app.services.blockchain_service import BlockchainService
from app.utils.utils import validate_transaction

bp = Blueprint('blockchain', __name__)
blockchain_service = BlockchainService()

@bp.route('/chain', methods=['GET'])
def get_chain():
    chain_data = blockchain_service.get_chain()
    return jsonify(chain_data), 200

@bp.route('/mine', methods=['GET'])
def mine():
    result = blockchain_service.mine()
    if not result:
        return jsonify({"message": "No transactions to mine"}), 400
    return jsonify({"message": f"Block #{result} is mined", "block": blockchain_service.get_last_block().__dict__}), 200

@bp.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify({"message": "Missing values"}), 400

    if not validate_transaction(values):
        return jsonify({"message": "Invalid transaction"}), 400

    index = blockchain_service.add_transaction(values)
    return jsonify({"message": f"Transaction will be added to Block {index}"}), 201

@bp.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return jsonify({"message": "Error: Please supply a valid list of nodes"}), 400

    for node in nodes:
        blockchain_service.register_node(node)

    return jsonify({"message": "New nodes have been added", "total_nodes": list(blockchain_service.nodes)}), 201

@bp.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain_service.resolve_conflicts()

    if replaced:
        return jsonify({"message": "Our chain was replaced", "new_chain": blockchain_service.get_chain()}), 200
    else:
        return jsonify({"message": "Our chain is authoritative", "chain": blockchain_service.get_chain()}), 200
