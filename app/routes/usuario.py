from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.usuario import Usuario
from app.models.especialidade import Especialidade
from app.utils.permissoes import somente_admin
from app.forms.usuario_form import FormEditarUsuario
from app import db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios/listar')
@login_required
@somente_admin
def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template('usuario_lista.html', usuarios=usuarios)

@usuario_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@somente_admin
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    especialidades_ativas = Especialidade.query.filter_by(ativa=True).all()
    form = FormEditarUsuario(obj=usuario)
    form.especialidades.choices = [(e.id, e.nome) for e in especialidades_ativas]

    if form.validate_on_submit():
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.papel = form.papel.data
        usuario.telefone = form.telefone.data
        usuario.oab_numero = form.oab_numero.data
        usuario.oab_uf = form.oab_uf.data
        usuario.especialidades = Especialidade.query.filter(Especialidade.id.in_(form.especialidades.data)).all()
        if form.senha.data:
            usuario.set_senha(form.senha.data)
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuario.listar_usuarios'))
    return render_template('usuario_form.html', form=form, editar=True)

@usuario_bp.route('/usuarios/excluir/<int:id>', methods=['POST'])
@login_required
@somente_admin
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso.', 'success')
    return redirect(url_for('usuario.listar_usuarios'))