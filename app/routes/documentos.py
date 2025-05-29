from flask import Blueprint, send_file, abort, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.forms.template_form import FormUploadTemplate, FormEditarTemplate
from app.models.template_documento import TemplateDocumento
from app.utils.permissoes import somente_admin
from app.models.cliente import Cliente
from app.utils.documentos import preencher_template_com_dados_personalizado
from app import db

documentos_bp = Blueprint('documentos', __name__)

@documentos_bp.route('/templates/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@somente_admin
def editar_template(id):
    template = TemplateDocumento.query.get_or_404(id)
    form = FormEditarTemplate(obj=template)
    if form.validate_on_submit():
        template.nome = form.nome.data
        db.session.commit()
        flash('Template atualizado com sucesso!', 'success')
        return redirect(url_for('documentos.listar_templates'))
    return render_template('template_form.html', form=form, editar=True)

@documentos_bp.route('/templates/atualizar-nome/<int:template_id>', methods=['POST'])
@login_required
def atualizar_nome_template(template_id):
    data = request.get_json()
    novo_nome = data.get('nome')
    if not novo_nome:
        return jsonify({'success': False, 'error': 'Nome não pode ser vazio.'})

    template = TemplateDocumento.query.get(template_id)
    if not template:
        return jsonify({'success': False, 'error': 'Template não encontrado.'})

    template.nome = novo_nome
    db.session.commit()
    return jsonify({'success': True})

@documentos_bp.route('/templates/novo', methods=['GET', 'POST'])
@login_required
@somente_admin
def novo_template():
    form = FormUploadTemplate()
    if form.validate_on_submit():
        arquivo = form.arquivo.data
        filename = secure_filename(arquivo.filename)
        caminho = os.path.join(current_app.root_path, 'templates', 'documentos', filename)
        arquivo.save(caminho)

        novo = TemplateDocumento(
            nome=form.nome.data,
            arquivo=filename,
            data_criacao=datetime.utcnow()
        )
        db.session.add(novo)
        db.session.commit()

        flash('Template adicionado com sucesso!', 'success')
        return redirect(url_for('painel.dashboard'))

    return render_template('template_form.html', form=form)


@documentos_bp.route('/templates/listar')
@login_required
def listar_templates():
    templates = TemplateDocumento.query.order_by(TemplateDocumento.data_criacao.desc()).all()
    return render_template('template_lista.html', templates=templates)


@documentos_bp.route('/templates/<int:id>/visualizar')
@login_required
def visualizar_template(id):
    template = TemplateDocumento.query.get_or_404(id)
    caminho = os.path.join(current_app.root_path, 'templates', 'documentos', template.arquivo)
    return send_file(
        caminho,
        as_attachment=False,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        download_name=template.arquivo
    )


@documentos_bp.route('/templates/<int:id>/download')
@login_required
def download_template(id):
    template = TemplateDocumento.query.get_or_404(id)
    caminho = os.path.join(current_app.root_path, 'templates', 'documentos', template.arquivo)
    return send_file(
        caminho,
        as_attachment=True,
        download_name=template.arquivo,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


@documentos_bp.route('/templates/<int:id>/excluir', methods=['POST'])
@login_required
@somente_admin
def excluir_template(id):
    template = TemplateDocumento.query.get_or_404(id)
    caminho = os.path.join(current_app.root_path, 'templates', 'documentos', template.arquivo)

    if os.path.exists(caminho):
        os.remove(caminho)

    db.session.delete(template)
    db.session.commit()

    flash('Template excluído com sucesso.', 'success')
    return redirect(url_for('documentos.listar_templates'))


@documentos_bp.route('/documentos/<int:cliente_id>/template/<int:template_id>')
@login_required
def gerar_documento_personalizado(cliente_id, template_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    template = TemplateDocumento.query.get_or_404(template_id)

    caminho_template = os.path.join(current_app.root_path, 'templates', 'documentos', template.arquivo)
    if not os.path.exists(caminho_template):
        abort(404, description="Arquivo de template não encontrado.")

    documento_stream = preencher_template_com_dados_personalizado(cliente, caminho_template)
    if not documento_stream:
        abort(500, description="Erro ao gerar documento personalizado.")

    return send_file(
        documento_stream,
        as_attachment=True,
        download_name=f'{template.nome}_{cliente.nome_completo}.docx',
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


@documentos_bp.route('/documentos/gerar-por-template', methods=['POST'])
@login_required
def gerar_documento_redirect():
    cliente_id = request.form.get('cliente_id')
    template_id = request.form.get('template_id')

    if not cliente_id or not template_id:
        flash('Cliente ou template não informado.', 'danger')
        return redirect(url_for('cliente.lista_clientes'))

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        flash('Cliente não encontrado.', 'danger')
        return redirect(url_for('cliente.lista_clientes'))

    template = TemplateDocumento.query.get(template_id)
    if not template:
        flash('Modelo de documento inválido.', 'danger')
        return redirect(url_for('cliente.cliente_detalhe', cliente_id=cliente_id))

    return redirect(url_for('documentos.gerar_documento_personalizado', cliente_id=cliente_id, template_id=template_id))