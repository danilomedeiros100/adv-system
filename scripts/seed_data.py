from app import create_app, db
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from datetime import date
import random

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Criar usuários
    admin = Usuario(nome="Admin", email="admin@teste.com", papel="administrador")
    admin.set_senha("123456")

    advogado = Usuario(nome="Advogado Exemplo", email="adv@teste.com", papel="advogado")
    advogado.set_senha("123456")

    secretario = Usuario(nome="Secretário Exemplo", email="sec@teste.com", papel="recepcionista")
    secretario.set_senha("123456")

    db.session.add_all([admin, advogado, secretario])

    tipos = ["trabalhista", "previdenciario", "consumidor", "civel"]

    for i in range(1, 11):
        cliente = Cliente(
            nome_completo=f"Cliente {i}",
            cpf=f"{i:011d}",
            rg=f"{1000+i}",
            telefone=f"(81)9{i:08d}",
            email=f"cliente{i}@teste.com",
            endereco=f"Rua Exemplo {i}",
            estado_civil="solteiro",
            profissao="Profissão Exemplo",
            nacionalidade="Brasileira",
            naturalidade="Recife",
            data_nascimento=date(1990, 1, i if i <= 28 else 28),
            nome_pai=f"Pai Cliente {i}",
            nome_mae=f"Mãe Cliente {i}",
            tipo_causa=random.choice(tipos)
        )
        db.session.add(cliente)

    from app.models.template_documento import TemplateDocumento
    from datetime import datetime

    templates_fixos = [
        ("Procuração", "procuracao.docx"),
        ("Contrato Trabalhista", "contrato_trabalhista.docx"),
        ("Contrato Previdenciário", "contrato_previdenciario.docx"),
    ]

    for nome, arquivo in templates_fixos:
        template = TemplateDocumento(nome=nome, arquivo=arquivo, data_criacao=datetime.utcnow())
        db.session.add(template)

    from app.models.especialidade import Especialidade

    especialidades_iniciais = [
        "Direito do Trabalho",
        "Direito Civil",
        "Direito Previdenciário",
        "Direito do Consumidor",
        "Direito Empresarial",
    ]

    for nome in especialidades_iniciais:
        existe = Especialidade.query.filter_by(nome=nome).first()
        if not existe:
            e = Especialidade(nome=nome, ativa=True)
            db.session.add(e)

    db.session.commit()
    print("Usuários, clientes, templates e especialidades de exemplo criados com sucesso!")