from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.especialidade import Especialidade
from app.utils.permissoes import somente_admin
from app import db

especialidade_bp = Blueprint('especialidade', __name__)

@especialidade_bp.route('/especialidades/listar')
@login_required
@somente_admin
def listar_especialidades():
    especialidades = Especialidade.query.order_by(Especialidade.nome).all()
    return render_template('especialidade_lista.html', especialidades=especialidades)

@especialidade_bp.route('/especialidades/novo', methods=['GET', 'POST'])
@login_required
@somente_admin
def nova_especialidade():
    if request.method == 'POST':
        nome = request.form.get('nome')
        ativa = 'ativa' in request.form
        if not nome:
            flash('O nome da especialidade é obrigatório.', 'danger')
            return redirect(url_for('especialidade.nova_especialidade'))
        existe = Especialidade.query.filter_by(nome=nome).first()
        if existe:
            flash('Especialidade já cadastrada.', 'warning')
            return redirect(url_for('especialidade.nova_especialidade'))
        nova = Especialidade(nome=nome, ativa=ativa)
        db.session.add(nova)
        db.session.commit()
        flash('Especialidade cadastrada com sucesso!', 'success')
        return redirect(url_for('especialidade.listar_especialidades'))
    return render_template('especialidade_form.html', editar=False)

@especialidade_bp.route('/especialidades/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@somente_admin
def editar_especialidade(id):
    especialidade = Especialidade.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        ativa = 'ativa' in request.form
        if not nome:
            flash('O nome da especialidade é obrigatório.', 'danger')
            return redirect(url_for('especialidade.editar_especialidade', id=id))
        existe = Especialidade.query.filter(Especialidade.nome==nome, Especialidade.id != id).first()
        if existe:
            flash('Outra especialidade com este nome já existe.', 'warning')
            return redirect(url_for('especialidade.editar_especialidade', id=id))
        especialidade.nome = nome
        especialidade.ativa = ativa
        db.session.commit()
        flash('Especialidade atualizada com sucesso!', 'success')
        return redirect(url_for('especialidade.listar_especialidades'))
    return render_template('especialidade_form.html', especialidade=especialidade, editar=True)

@especialidade_bp.route('/especialidades/excluir/<int:id>', methods=['POST'])
@login_required
@somente_admin
def excluir_especialidade(id):
    especialidade = Especialidade.query.get_or_404(id)
    db.session.delete(especialidade)
    db.session.commit()
    flash('Especialidade excluída com sucesso.', 'success')
    return redirect(url_for('especialidade.listar_especialidades'))