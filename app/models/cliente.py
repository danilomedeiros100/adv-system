from datetime import datetime
from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    rg = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    cep = db.Column(db.String(9))
    estado = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    endereco = db.Column(db.String(150))
    estado_civil = db.Column(db.String(30))
    profissao = db.Column(db.String(50))
    nacionalidade = db.Column(db.String(50))
    naturalidade = db.Column(db.String(50))
    data_nascimento = db.Column(db.Date)
    nome_pai = db.Column(db.String(100))
    nome_mae = db.Column(db.String(100))
    tipo_causa = db.Column(db.String(30), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Cliente {self.nome_completo} - {self.tipo_causa}>"