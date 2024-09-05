import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    NODE_ADDRESS = os.environ.get('NODE_ADDRESS') or 'http://localhost:5000'