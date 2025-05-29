

from app import db
from datetime import datetime

class TemplateDocumento(db.Model):
    __tablename__ = 'templates_documentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    arquivo = db.Column(db.String(200), nullable=False)  # nome do arquivo .docx
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TemplateDocumento {self.nome}>'