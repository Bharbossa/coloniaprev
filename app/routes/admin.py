from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Usuario, Documento, Servidor, LeiDecreto, db
from app import bcrypt

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def require_admin():
    if not current_user.has_panel_access():
        flash('Acesso Negado. Esta área é restrita a administradores.', 'danger')
        return redirect(url_for('public.index'))

@bp.route('/dashboard')
def dashboard():
    total_usuarios = Usuario.query.count()
    total_documentos = Documento.query.count()
    total_servidores = Servidor.query.count()
    total_leis = LeiDecreto.query.count()

    doc_tipos_brutos = db.session.query(Documento.tipo, db.func.count(Documento.id)).group_by(Documento.tipo).all()
    labels = [d[0] for d in doc_tipos_brutos]
    data = [d[1] for d in doc_tipos_brutos]

    return render_template('admin_dashboard.html', 
                            total_usuarios=total_usuarios, 
                            total_documentos=total_documentos, 
                            total_servidores=total_servidores, 
                            total_leis=total_leis,
                            chart_labels=labels,
                            chart_data=data)

@bp.route('/usuarios')
def usuarios():
    if not current_user.is_admin():
        flash('Acesso Negado. Apenas o Administrador Geral pode gerenciar usuários.', 'danger')
        return redirect(url_for('admin.dashboard'))
    usuarios = Usuario.query.all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@bp.route('/usuarios/novo', methods=['GET', 'POST'])
def novo_usuario():
    if not current_user.is_admin():
        flash('Acesso Negado.', 'danger')
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo', 'cidadao')

        if Usuario.query.filter_by(email=email).first():
            flash('Este email já está cadastrado.', 'danger')
        else:
            hashed_pw = bcrypt.generate_password_hash(senha).decode('utf-8')
            novo = Usuario(nome=nome, email=email, senha=hashed_pw, tipo=tipo)
            db.session.add(novo)
            db.session.commit()
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('admin.usuarios'))
    return render_template('admin_usuario_form.html')

@bp.route('/usuarios/editar/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    if not current_user.is_admin():
        flash('Acesso Negado.', 'danger')
        return redirect(url_for('admin.dashboard'))
    user = Usuario.query.get_or_404(user_id)
    if request.method == 'POST':
        user.nome = request.form.get('nome')
        user.email = request.form.get('email')
        user.tipo = request.form.get('tipo')
        nova_senha = request.form.get('senha')
        if nova_senha:
            user.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin.usuarios'))
    return render_template('admin_usuario_form.html', user=user)

@bp.route('/usuarios/excluir/<int:user_id>')
def excluir_usuario(user_id):
    if not current_user.is_admin():
        flash('Acesso Negado.', 'danger')
        return redirect(url_for('admin.dashboard'))
    if user_id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('admin.usuarios'))
        
    user = Usuario.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído.', 'success')
    return redirect(url_for('admin.usuarios'))

import os
from werkzeug.utils import secure_filename
from flask import current_app

@bp.route('/documentos')
def documentos():
    documentos = Documento.query.all()
    return render_template('admin_documentos.html', documentos=documentos)

@bp.route('/documentos/novo', methods=['GET', 'POST'])
def novo_documento():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        tipo = request.form.get('tipo')
        arquivo = request.files.get('arquivo')
        
        if arquivo and arquivo.filename != '':
            filename = secure_filename(arquivo.filename)
            file_data = arquivo.read()
            
            novo = Documento(titulo=titulo, tipo=tipo, arquivo=filename, dados_arquivo=file_data)
            db.session.add(novo)
            db.session.commit()
            flash('Documento enviado com sucesso!', 'success')
            return redirect(url_for('admin.documentos'))
        else:
            flash('Você deve selecionar um arquivo PDF.', 'danger')
            
    return render_template('admin_documento_form.html')

@bp.route('/documentos/excluir/<int:doc_id>')
def excluir_documento(doc_id):
    doc = Documento.query.get_or_404(doc_id)
    
    # Excluir o arquivo fixamente se existir no diretório antigo (legado)
    filepath = os.path.join(current_app.root_path, 'static', 'uploads', doc.arquivo)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception:
            pass
            
    db.session.delete(doc)
    db.session.commit()
    flash('Documento excluído!', 'success')
    return redirect(url_for('admin.documentos'))

@bp.route('/servidores')
def servidores():
    servidores = Servidor.query.all()
    return render_template('admin_servidores.html', servidores=servidores)

@bp.route('/servidores/novo', methods=['GET', 'POST'])
def novo_servidor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cargo = request.form.get('cargo')
        tipo = request.form.get('tipo', 'ativo')
        situacao = request.form.get('situacao', 'ativo')
        salario = float(request.form.get('salario', 0.0))

        novo = Servidor(nome=nome, cargo=cargo, tipo=tipo, situacao=situacao, salario=salario)
        db.session.add(novo)
        db.session.commit()
        flash('Servidor cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.servidores'))
    return render_template('admin_servidor_form.html')

@bp.route('/servidores/editar/<int:serv_id>', methods=['GET', 'POST'])
def editar_servidor(serv_id):
    servidor = Servidor.query.get_or_404(serv_id)
    if request.method == 'POST':
        servidor.nome = request.form.get('nome')
        servidor.cargo = request.form.get('cargo')
        servidor.tipo = request.form.get('tipo')
        servidor.situacao = request.form.get('situacao')
        servidor.salario = float(request.form.get('salario', 0.0))
        
        db.session.commit()
        flash('Servidor atualizado com sucesso!', 'success')
        return redirect(url_for('admin.servidores'))
    return render_template('admin_servidor_form.html', servidor=servidor)

@bp.route('/servidores/excluir/<int:serv_id>')
def excluir_servidor(serv_id):
    servidor = Servidor.query.get_or_404(serv_id)
    db.session.delete(servidor)
    db.session.commit()
    flash('Servidor excluído.', 'success')
    return redirect(url_for('admin.servidores'))

@bp.route('/leis')
def leis():
    leis = LeiDecreto.query.all()
    return render_template('admin_leis.html', leis=leis)

@bp.route('/leis/novo', methods=['GET', 'POST'])
def nova_lei():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        tipo = request.form.get('tipo')
        arquivo = request.files.get('arquivo')
        
        if arquivo and arquivo.filename != '':
            filename = secure_filename(arquivo.filename)
            file_data = arquivo.read()
            
            novo = LeiDecreto(titulo=titulo, tipo=tipo, arquivo=filename, dados_arquivo=file_data)
            db.session.add(novo)
            db.session.commit()
            flash('Lei ou Decreto publicado com sucesso!', 'success')
            return redirect(url_for('admin.leis'))
        else:
            flash('Você deve selecionar um arquivo PDF.', 'danger')
            
    return render_template('admin_lei_form.html')

@bp.route('/leis/excluir/<int:lei_id>')
def excluir_lei(lei_id):
    lei = LeiDecreto.query.get_or_404(lei_id)
    filepath = os.path.join(current_app.root_path, 'static', 'uploads', lei.arquivo)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception:
            pass
            
    db.session.delete(lei)
    db.session.commit()
    flash('Documento oficial excluído!', 'success')
    return redirect(url_for('admin.leis'))

import base64

@bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        foto = request.files.get('foto')

        if nova_senha or senha_atual:
            if not bcrypt.check_password_hash(current_user.senha, senha_atual):
                flash('Senha atual incorreta.', 'danger')
                return redirect(url_for('admin.perfil'))
            if nova_senha != confirmar_senha:
                flash('As novas senhas não conferem.', 'danger')
                return redirect(url_for('admin.perfil'))
            if nova_senha:
                current_user.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')

        if foto and foto.filename != '':
            image_bytes = foto.read()
            encoded_string = base64.b64encode(image_bytes).decode('utf-8')
            mime_type = foto.content_type
            current_user.foto = f"data:{mime_type};base64,{encoded_string}"

        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('admin.perfil'))

    return render_template('admin_perfil.html')
