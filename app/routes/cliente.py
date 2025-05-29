from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from app.forms.cliente_form import ClienteForm
from app.models.cliente import Cliente
from app.models.template_documento import TemplateDocumento
from app import db

cliente_bp = Blueprint('cliente', __name__)

class FormSelecionarTemplate(FlaskForm):
    template_id = SelectField('Modelo de Documento', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Gerar Documento')

@cliente_bp.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
def novo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        # Verificar unicidade de CPF, e-mail e telefone
        cpf_existente = Cliente.query.filter_by(cpf=form.cpf.data).first()
        email_existente = Cliente.query.filter_by(email=form.email.data).first()
        telefone_existente = Cliente.query.filter_by(telefone=form.telefone.data).first()

        if cpf_existente:
            flash('Já existe um cliente cadastrado com este CPF.', 'danger')
            return render_template('cliente_form.html', form=form)

        if email_existente:
            flash('Já existe um cliente cadastrado com este e-mail.', 'danger')
            return render_template('cliente_form.html', form=form)

        if telefone_existente:
            flash('Já existe um cliente cadastrado com este telefone.', 'danger')
            return render_template('cliente_form.html', form=form)

        novo = Cliente(
            nome_completo=form.nome_completo.data,
            cpf=form.cpf.data,
            rg=form.rg.data,
            telefone=form.telefone.data,
            email=form.email.data,
            cep=form.cep.data,
            endereco=form.endereco.data,
            estado=form.estado.data,
            cidade=form.cidade.data,
            estado_civil=form.estado_civil.data,
            profissao=form.profissao.data,
            nacionalidade=form.nacionalidade.data,
            naturalidade=form.naturalidade.data,
            data_nascimento=form.data_nascimento.data,
            nome_pai=form.nome_pai.data,
            nome_mae=form.nome_mae.data,
            tipo_causa=form.tipo_causa.data,
            data_cadastro=datetime.utcnow(),
            ultima_atualizacao=datetime.utcnow()
        )
        db.session.add(novo)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('cliente.cliente_detalhe', cliente_id=novo.id))
    return render_template('cliente_form.html', form=form)

@cliente_bp.route('/clientes')
@login_required
def lista_clientes():
    q = request.args.get('q', '').strip()
    tipo = request.args.get('tipo', '').strip().lower()
    ordenar_por = request.args.get('ordem', 'data')
    de_data = request.args.get('de')
    ate_data = request.args.get('ate')

    query = Cliente.query

    if q:
        if q.isdigit():
            query = query.filter(Cliente.id == int(q))
        else:
            query = query.filter(
                (Cliente.nome_completo.ilike(f'%{q}%')) | (Cliente.cpf.ilike(f'%{q}%'))
            )

    if tipo:
        query = query.filter(Cliente.tipo_causa.ilike(f'%{tipo}%'))

    if de_data:
        try:
            de = datetime.strptime(de_data, '%Y-%m-%d')
            query = query.filter(Cliente.data_cadastro >= de)
        except ValueError:
            pass

    if ate_data:
        try:
            ate = datetime.strptime(ate_data, '%Y-%m-%d')
            query = query.filter(Cliente.data_cadastro <= ate)
        except ValueError:
            pass

    if ordenar_por == 'nome':
        query = query.order_by(Cliente.nome_completo.asc())
    else:
        query = query.order_by(Cliente.data_cadastro.desc())

    clientes = query.all()
    return render_template('cliente_lista.html', clientes=clientes)

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def cliente_detalhe(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    data_cadastro_formatada = cliente.data_cadastro.strftime('%d/%m/%Y') if cliente.data_cadastro else None
    ultima_atualizacao_formatada = cliente.ultima_atualizacao.strftime('%d/%m/%Y %H:%M:%S') if cliente.ultima_atualizacao else None

    templates = TemplateDocumento.query.order_by(TemplateDocumento.data_criacao.desc()).all()
    form_template = FormSelecionarTemplate()
    form_template.template_id.choices = [(t.id, t.nome) for t in templates]

    if form_template.validate_on_submit():
        return redirect(url_for('documentos.gerar_documento_personalizado',
                                cliente_id=cliente.id, template_id=form_template.template_id.data))

    return render_template(
        'cliente_detalhe.html',
        cliente=cliente,
        data_cadastro_formatada=data_cadastro_formatada,
        ultima_atualizacao_formatada=ultima_atualizacao_formatada,
        form=form_template,
        templates=templates  # <-- Enviando templates explicitamente
    )


# Rota para editar cliente existente
@cliente_bp.route('/clientes/<int:cliente_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form = ClienteForm(obj=cliente)

    if form.validate_on_submit():
        # Verificar unicidade de CPF, e-mail e telefone (excluindo o próprio cliente)
        cpf_existente = Cliente.query.filter(Cliente.cpf == form.cpf.data, Cliente.id != cliente.id).first()
        email_existente = Cliente.query.filter(Cliente.email == form.email.data, Cliente.id != cliente.id).first()
        telefone_existente = Cliente.query.filter(Cliente.telefone == form.telefone.data, Cliente.id != cliente.id).first()

        if cpf_existente:
            flash('Já existe outro cliente com este CPF.', 'danger')
            return render_template('cliente_form.html', form=form, editar=True, cliente=cliente)

        if email_existente:
            flash('Já existe outro cliente com este e-mail.', 'danger')
            return render_template('cliente_form.html', form=form, editar=True, cliente=cliente)

        if telefone_existente:
            flash('Já existe outro cliente com este telefone.', 'danger')
            return render_template('cliente_form.html', form=form, editar=True, cliente=cliente)

        cliente.nome_completo = form.nome_completo.data
        cliente.cpf = form.cpf.data
        cliente.rg = form.rg.data
        cliente.telefone = form.telefone.data
        cliente.email = form.email.data
        cliente.cep = form.cep.data
        cliente.endereco = form.endereco.data
        cliente.estado = form.estado.data
        cliente.cidade = form.cidade.data
        cliente.estado_civil = form.estado_civil.data
        cliente.profissao = form.profissao.data
        cliente.nacionalidade = form.nacionalidade.data
        cliente.naturalidade = form.naturalidade.data
        cliente.data_nascimento = form.data_nascimento.data
        cliente.nome_pai = form.nome_pai.data
        cliente.nome_mae = form.nome_mae.data
        cliente.tipo_causa = form.tipo_causa.data
        cliente.ultima_atualizacao = datetime.utcnow()
        db.session.commit()
        flash('Dados do cliente atualizados com sucesso!', 'success')
        return redirect(url_for('cliente.cliente_detalhe', cliente_id=cliente.id))

    return render_template('cliente_form.html', form=form, editar=True, cliente=cliente)