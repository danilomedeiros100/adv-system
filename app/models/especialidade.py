from app import db  # Importação direta e simples

usuario_especialidade = db.Table(
    'usuario_especialidade',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('especialidade_id', db.Integer, db.ForeignKey('especialidade.id'), primary_key=True)
)

class Especialidade(db.Model):
    __tablename__ = 'especialidade'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    ativa = db.Column(db.Boolean, default=True, nullable=False)

    usuarios = db.relationship('Usuario', secondary=usuario_especialidade, back_populates='especialidades')

    def __repr__(self):
        return f"<Especialidade {self.nome}>"