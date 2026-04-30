from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import Usuario
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            if user.is_admin():
                login_user(user)
                next_page = request.args.get('next')
                flash('Login efetuado com sucesso!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
            else:
                flash('Acesso negado. Apenas o administrador geral tem acesso.', 'danger')
        else:
            flash('Login não efetuado. Verifique e-mail e senha.', 'danger')
    return render_template('login.html', title='Login Restrito', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

