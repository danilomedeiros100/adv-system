from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp
from wtforms import ValidationError


class ClienteForm(FlaskForm):
    nome_completo = StringField('Nome completo', validators=[DataRequired(), Length(max=50)])

    cpf = StringField('CPF', validators=[
        DataRequired(),
        Length(min=11, max=11),
        Regexp(r'^\d{11}$', message='CPF deve conter exatamente 11 dígitos numéricos')
    ])

    rg = StringField('RG', validators=[Optional(), Length(max=20)])

    telefone = StringField('Telefone', validators=[
        Optional(),
        Regexp(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$', message='Formato de telefone inválido')
    ])

    email = StringField('Email', validators=[Optional(), Email(), Length(max=50)])

    endereco = StringField('Endereço', validators=[Optional(), Length(max=50)])

    estado_civil = SelectField('Estado civil', choices=[
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
        ('uniao_estavel', 'União Estável')
    ], validators=[Optional()])

    profissao = StringField('Profissão', validators=[Optional(), Length(max=50)])

    nacionalidade = StringField('Nacionalidade', validators=[Optional(), Length(max=50)])

    naturalidade = StringField('Naturalidade', validators=[Optional(), Length(max=30)])

    data_nascimento = DateField('Data de nascimento', format='%Y-%m-%d', validators=[Optional()])

    nome_pai = StringField('Nome do Pai', validators=[Optional(), Length(max=50)])

    nome_mae = StringField('Nome da Mãe', validators=[Optional(), Length(max=50)])

    tipo_causa = SelectField('Tipo de causa', choices=[
        ('trabalhista', 'Trabalhista'),
        ('previdenciario', 'Previdenciário'),
        ('consumidor', 'Consumidor'),
        ('civel', 'Cível')
    ], validators=[DataRequired()])

    cep = StringField('CEP', validators=[Optional(), Length(min=8, max=9)])

    estado = StringField('Estado', validators=[Optional(), Length(max=50)])

    cidade = StringField('Cidade', validators=[Optional(), Length(max=50)])

    submit = SubmitField('Cadastrar Cliente')

    def validate_cpf(self, field):
        cpf = field.data
        if cpf == cpf[0] * 11:
            raise ValidationError('CPF inválido.')
        soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma1 * 10 % 11) % 10
        soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma2 * 10 % 11) % 10
        if not (int(cpf[9]) == digito1 and int(cpf[10]) == digito2):
            raise ValidationError('CPF inválido.')