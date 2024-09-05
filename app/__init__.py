from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.models.blockchain import Blockchain
from app.routes.blockchain_routes import blockchain_bp
from app.routes.node_routes import node_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    app.blockchain = Blockchain()

    app.register_blueprint(blockchain_bp)
    app.register_blueprint(node_bp)

    return app
