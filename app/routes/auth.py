from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.forms.login_form import LoginForm
from app.models.usuario import Usuario
from app import db, login_manager
from app.forms.usuario_form import UsuarioForm
from app.utils.permissoes import somente_admin

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.verificar_senha(form.senha.data):
            login_user(usuario)
            flash('Login realizado com sucesso.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('painel.dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@somente_admin
def novo_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        existente = Usuario.query.filter_by(email=form.email.data).first()
        if existente:
            flash('E-mail já cadastrado. Escolha outro.', 'danger')
            return render_template('usuario_form.html', form=form)

        novo = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            papel=form.papel.data,
            oab_numero=form.oab_numero.data,
            oab_uf=form.oab_uf.data,
            especialidade=form.especialidade.data,
            telefone=form.telefone.data
        )
        novo.set_senha(form.senha.data)
        db.session.add(novo)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('usuario.listar_usuarios'))
    return render_template('usuario_form.html', form=form)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))