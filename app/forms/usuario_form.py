from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, Optional

class UsuarioForm(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    senha = PasswordField('Senha', validators=[Optional(), Length(min=6)])
    papel = SelectField('Papel', choices=[
        ('advogado', 'Advogado'),
        ('recepcionista', 'Recepcionista'),
        ('administrador', 'Administrador')
    ], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[Length(max=20)])
    oab_numero = StringField('Número da OAB', validators=[Length(max=20)])
    oab_uf = SelectField('UF da OAB', choices=[
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'),
        ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'),
        ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'),
        ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'),
        ('SE', 'SE'), ('TO', 'TO')
    ])
    especialidades = SelectMultipleField('Especialidades', coerce=int, validators=[])
    submit = SubmitField('Cadastrar Usuário')

class FormEditarUsuario(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    senha = PasswordField('Senha', validators=[Optional(), Length(min=6)])
    papel = SelectField('Papel', choices=[
        ('advogado', 'Advogado'),
        ('recepcionista', 'Recepcionista'),
        ('administrador', 'Administrador')
    ], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[Length(max=20)])
    oab_numero = StringField('Número da OAB', validators=[Length(max=20)])
    oab_uf = SelectField('UF da OAB', choices=[
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'),
        ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'),
        ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'),
        ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'),
        ('SE', 'SE'), ('TO', 'TO')
    ])
    especialidades = SelectMultipleField('Especialidades', coerce=int, validators=[])
    submit = SubmitField('Salvar Alteração')
