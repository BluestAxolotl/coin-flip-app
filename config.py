import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'CoinFlipDB.sqlite')
    DEBUG = True
