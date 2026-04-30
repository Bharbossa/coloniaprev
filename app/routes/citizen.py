from flask import Blueprint, render_template, send_file, current_app, abort, redirect, url_for, flash
import os
import io
from flask_login import login_required, current_user
from app.models import Documento, HistoricoDownload, db

bp = Blueprint('citizen', __name__, url_prefix='/cidadao')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Na vida real filtraria por usuário, mas estamos fazendo geral primeiro
    documentos = Documento.query.order_by(Documento.data_upload.desc()).all()
    historico = HistoricoDownload.query.filter_by(usuario_id=current_user.id).order_by(HistoricoDownload.data_download.desc()).limit(5).all()
    return render_template('citizen_dashboard.html', documentos=documentos, historico=historico)

@bp.route('/download/<int:doc_id>')
@login_required
def download_doc(doc_id):
    doc = Documento.query.get_or_404(doc_id)
    
    # Registra no histórico
    hist = HistoricoDownload(usuario_id=current_user.id, documento_id=doc.id)
    db.session.add(hist)
    db.session.commit()
    
    if doc.dados_arquivo:
        return send_file(io.BytesIO(doc.dados_arquivo), download_name=doc.arquivo, as_attachment=True)
    else:
        flash('Arquivo PDF ausente no servidor. Peça ao administrador para reenviar o arquivo.', 'danger')
        return redirect(url_for('citizen.dashboard'))
