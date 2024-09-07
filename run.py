from app import create_app
from cli import cli

app = create_app()

if __name__ == '__main__':
    cli(obj=app)