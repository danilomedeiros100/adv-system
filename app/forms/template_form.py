from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class FormUploadTemplate(FlaskForm):
    nome = StringField('Nome do Template', validators=[DataRequired(), Length(max=100)])
    arquivo = FileField('Arquivo .docx', validators=[
        FileAllowed(['docx'], 'Apenas arquivos .docx são permitidos')
    ])
    submit = SubmitField('Salvar Template')

class FormEditarTemplate(FlaskForm):
    nome = StringField('Nome do Template', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Salvar Alteração')