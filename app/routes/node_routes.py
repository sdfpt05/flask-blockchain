
from flask import Blueprint, jsonify, request, current_app
from app.services.node_service import NodeService

node_bp = Blueprint('node', __name__)
node_service = NodeService()

@node_bp.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return jsonify({'message': 'Error: Please supply a valid list of nodes'}), 400

    for node in nodes:
        node_service.register_node(current_app.blockchain, node)

    return jsonify({
        'message': 'New nodes have been added',
        'total_nodes': list(current_app.blockchain.nodes),
    }), 201

@node_bp.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = node_service.resolve_conflicts(current_app.blockchain)

    if replaced:
        return jsonify({
            'message': 'Our chain was replaced',
            'new_chain': node_service.get_chain(current_app.blockchain)
        }), 200
    else:
        return jsonify({
            'message': 'Our chain is authoritative',
            'chain': node_service.get_chain(current_app.blockchain)
        }), 200