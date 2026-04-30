import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Usuario

app = create_app()
with app.app_context():
    usuarios = Usuario.query.all()
    print(f"Usuarios encontrados: {len(usuarios)}")
    for u in usuarios:
        print(f"- {u.email}")
