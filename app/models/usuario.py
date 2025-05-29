from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.especialidade import Especialidade

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    papel = db.Column(db.String(20), nullable=False)  # recepcionista, advogado, administrador
    telefone = db.Column(db.String(20))
    oab_numero = db.Column(db.String(20))
    oab_uf = db.Column(db.String(2))
    especialidades = db.relationship('Especialidade', secondary='usuario_especialidade', back_populates='usuarios')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.nome} - {self.papel}>"