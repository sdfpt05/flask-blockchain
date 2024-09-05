# Flask Blockchain

This project is a Flask-based implementation of a blockchain

## Features

- Advanced blockchain implementation with proof-of-work consensus
- RESTful API for interacting with the blockchain
- Transaction creation and validation
- Block mining
- Chain validation and conflict resolution
- Node registration and management
- CORS support for cross-origin requests
- Environment variable configuration
- Modular project structure following Flask best practices

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sdfpt05/flask-blockchain.git
cd advanced-blockchain-flask-app
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your configuration:

```bash
SECRET_KEY=your-secret-key
NODE_ADDRESS=http://localhost:5000
```

## Running the Application

To run the application, execute:

```bash
python run.py
```

The application will start on `http://localhost:5000`.

## API Endpoints

- GET `/chain`: Retrieve the full blockchain
- POST `/transactions/new`: Create a new transaction
- GET `/mine`: Mine a new block
- POST `/nodes/register`: Register new nodes in the network
- GET `/nodes/resolve`: Implement the consensus algorithm

## Testing

To run the tests, execute:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
