import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost:5432/Expense_db'

    SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_TRACK_MODIFICATIONS = False