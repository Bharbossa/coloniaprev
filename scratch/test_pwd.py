import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db, bcrypt
from app.models import Usuario

app = create_app()
with app.app_context():
    user = Usuario.query.filter_by(email='admin@coloniaprev.com.br').first()
    if user:
        print(f"User found: {user.email}")
        print(f"Password hash: {user.senha}")
        print(f"Check password '123456': {bcrypt.check_password_hash(user.senha, '123456')}")
        print(f"is_admin: {user.is_admin()}")
    else:
        print("User not found!")
