from flask import Blueprint, render_template, request, send_from_directory, current_app
import os
from app.models import Servidor, LeiDecreto

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/transparencia')
def transparencia():
    page = request.args.get('page', 1, type=int)
    busca = request.args.get('busca', '')
    query = Servidor.query.filter(Servidor.tipo.in_(['aposentado', 'pensionista']))
    if busca:
        query = query.filter(Servidor.nome.ilike(f'%{busca}%'))
    servidores = query.paginate(page=page, per_page=10)
    return render_template('transparencia.html', servidores=servidores, busca=busca)

@bp.route('/servidores')
def servidores():
    servidores = Servidor.query.all()
    return render_template('servidores.html', servidores=servidores)

@bp.route('/leis')
def leis():
    leis = LeiDecreto.query.order_by(LeiDecreto.data_publicacao.desc()).all()
    return render_template('leis.html', leis=leis)

@bp.route('/leis/download/<int:lei_id>')
def download_lei(lei_id):
    lei = LeiDecreto.query.get_or_404(lei_id)
    filepath = os.path.join(current_app.root_path, 'static', 'uploads', lei.arquivo)
    if os.path.exists(filepath):
        return send_from_directory(os.path.join(current_app.root_path, 'static', 'uploads'), lei.arquivo, as_attachment=True)
    return "Arquivo não encontrado", 404
