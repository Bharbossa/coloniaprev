from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default='cidadao') # admin / cidadao

    def is_admin(self):
        return self.tipo == 'admin'

class Documento(db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(100), nullable=False) # Contracheque, Informe, etc.
    arquivo = db.Column(db.String(200), nullable=False) # filename or path
    data_upload = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Servidor(db.Model):
    __tablename__ = 'servidores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(50), nullable=False) # aposentado / pensionista
    situacao = db.Column(db.String(50), default='Ativo')
    salario = db.Column(db.Float, nullable=False)

class LeiDecreto(db.Model):
    __tablename__ = 'leis_decretos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(100), nullable=False) # Lei, Decreto, Portaria
    arquivo = db.Column(db.String(200), nullable=False)
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class HistoricoDownload(db.Model):
    __tablename__ = 'historico_downloads'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)
    data_download = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref=db.backref('downloads', lazy=True))
    documento = db.relationship('Documento', backref=db.backref('downloads', lazy=True))
