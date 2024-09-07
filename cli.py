import click
from app import create_app
from app.models.blockchain import Blockchain

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = create_app()

@cli.command()
@click.pass_context
def printchain(ctx):
    """Print all the blocks of the blockchain."""
    blockchain = ctx.obj.blockchain
    for block in blockchain.chain:
        print(f"Block #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Previous hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("Transactions:")
        for tx in block.transactions:
            print(f"  {tx}")
        print("\n")

@cli.command()
@click.argument('address')
@click.pass_context
def getbalance(ctx, address):
    """Get the balance of an address."""
    blockchain = ctx.obj.blockchain
    balance = blockchain.get_balance(address)
    print(f"Balance of {address}: {balance}")

@cli.command()
@click.argument('from_address')
@click.argument('to_address')
@click.argument('amount', type=float)
@click.pass_context
def send(ctx, from_address, to_address, amount):
    """Send coins from one address to another."""
    blockchain = ctx.obj.blockchain
    tx = blockchain.create_transaction(from_address, to_address, amount)
    blockchain.add_transaction(tx)
    print(f"Transaction added: {tx.id}")

if __name__ == '__main__':
    cli()