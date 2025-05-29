from docxtpl import DocxTemplate
import io
import os
from flask import current_app

def render_template_para_stream(caminho_template, contexto):
    doc = DocxTemplate(caminho_template)
    doc.render(contexto)
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output

def gerar_procuracao(cliente):
    try:
        caminho_template = os.path.join("app", "templates", "documentos", "procuracao.docx")

        contexto = {
            "nome": cliente.nome_completo,
            "cpf": cliente.cpf,
            "rg": cliente.rg,
            "orgao": "SSP",  # Pode ser ajustado ou adicionado ao modelo Cliente no futuro
            "data_emissao": "01/01/2020",  # Exemplo fixo por enquanto
            "nacionalidade": cliente.nacionalidade,
            "naturalidade": cliente.naturalidade,
            "estado_civil": cliente.estado_civil,
            "profissao": cliente.profissao,
            "nascimento": cliente.data_nascimento.strftime('%d/%m/%Y') if cliente.data_nascimento else "",
            "filiacao": cliente.filiacao,
            "endereco": cliente.endereco,
            "cep": "00000-000"  # Valor fictício por enquanto
        }

        return render_template_para_stream(caminho_template, contexto)
    except Exception as e:
        print(f"Erro ao gerar procuração para {cliente.nome_completo}: {e}")
        return None

def gerar_contrato_trabalhista(cliente):
    try:
        caminho_template = os.path.join("app", "templates", "documentos", "contrato_trabalhista.docx")

        contexto = {
            "nome": cliente.nome_completo,
            "cpf": cliente.cpf,
            "endereco": cliente.endereco,
            "cep": "00000-000"
        }

        return render_template_para_stream(caminho_template, contexto)
    except Exception as e:
        print(f"Erro ao gerar contrato trabalhista para {cliente.nome_completo}: {e}")
        return None

def gerar_contrato_previdenciario(cliente):
    try:
        caminho_template = os.path.join("app", "templates", "documentos", "contrato_previdenciario.docx")

        contexto = {
            "nome": cliente.nome_completo,
            "cpf": cliente.cpf,
            "endereco": cliente.endereco,
            "cep": "00000-000"
        }

        return render_template_para_stream(caminho_template, contexto)
    except Exception as e:
        print(f"Erro ao gerar contrato previdenciário para {cliente.nome_completo}: {e}")
        return None

def gerar_contrato(cliente):
    if cliente.tipo_causa == 'trabalhista':
        return gerar_contrato_trabalhista(cliente)
    elif cliente.tipo_causa == 'previdenciario':
        return gerar_contrato_previdenciario(cliente)
    else:
        print("Tipo de causa não suportado para geração de contrato.")
        return None

def preencher_template_com_dados_personalizado(cliente, template):
    try:
        print("Iniciando preenchimento do template...")
        print("Cliente:", getattr(cliente, 'nome_completo', 'sem nome'))
        print("Template:", template)

        caminho_template = os.path.join(current_app.root_path, "templates", "documentos", template)
        if not os.path.exists(caminho_template):
            raise FileNotFoundError(f"Template não encontrado em: {caminho_template}")

        contexto = {
            "nome": cliente.nome_completo,
            "cpf": cliente.cpf,
            "rg": cliente.rg,
            "nacionalidade": cliente.nacionalidade,
            "naturalidade": cliente.naturalidade,
            "estado_civil": cliente.estado_civil,
            "profissao": cliente.profissao,
            "nascimento": cliente.data_nascimento.strftime('%d/%m/%Y') if cliente.data_nascimento else "",
            "filiacao": f"{cliente.nome_pai or ''} e {cliente.nome_mae or ''}",
            "endereco": cliente.endereco,
            "cep": cliente.cep,
            "cidade": cliente.cidade,
            "estado": cliente.estado,
            "email": cliente.email,
            "telefone": cliente.telefone
        }

        print("Contexto a ser renderizado:", contexto)
        resultado = render_template_para_stream(caminho_template, contexto)
        print("Documento gerado com sucesso.")
        return resultado
    except Exception as e:
        print(f"Erro ao preencher template {template} com dados do cliente {getattr(cliente, 'nome_completo', 'desconhecido')}: {e}")
        return None