from ecdsa import SigningKey, SECP256k1
import hashlib
import base58

class Wallet:
    def __init__(self):
        self._private_key = SigningKey.generate(curve=SECP256k1)
        self._public_key = self._private_key.get_verifying_key()

    @property
    def address(self):
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        return base58.b58encode_check(ripemd160_bpk).decode('ascii')

    def sign(self, message):
        return self._private_key.sign(message.encode())

    @staticmethod
    def verify(message, signature, public_key):
        return public_key.verify(signature, message.encode())

# Add wallet management to Blockchain class
class Blockchain:
    def __init__(self):
        # ... existing code ...
        self.wallets = {}

    def create_wallet(self):
        wallet = Wallet()
        self.wallets[wallet.address] = wallet
        return wallet.address

    def get_balance(self, address):
        # Implement balance calculation using UTXO set
        pass