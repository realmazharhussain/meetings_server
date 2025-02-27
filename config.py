import os

class Config:
    SECRET_KEY = 'your-secret-key'  # In production, use a secure secret key from environment variables
    
    # Setup SQLite database
    db_path = os.path.expanduser('~/.config/meetings/database.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False