from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators, PasswordField,ValidationError
from flask_wtf.file import FileField,FileRequired, FileAllowed
from flask_wtf import FlaskForm
from .models import Cadastrar




class CadastroClienteForm(FlaskForm):
    name = StringField('Nome: ')
    username = StringField('Usuario: ',[validators.DataRequired()])
    email= StringField('Email: ', [validators.DataRequired()])
    password = PasswordField,('Senha: ',[validators.DataRequired(), validators.EqualTo('confirm', message='Confirmar sua Senha')])
    confirm = PasswordField('Digite novamente sua senha: ',[validators.DataRequired()])
    country = StringField('País: ',[validators.DataRequired()])
    state = StringField('Estado: ',[validators.DataRequired()])
    city = StringField('Cidade: ',[validators.DataRequired()])
    contact = StringField('Contato: ', [validators.DataRequired()])
    address = StringField('Endereço: ', [validators.DataRequired()])
    zipcode = StringField('Caixa-Postal: ', [validators.DataRequired()])
    profile = FileField('Pefil', validators=[FileAllowed('jpg','png','gif', 'jpeg'), 'Apenas fotos'])


    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        if Cadastrar.query.filter_by(username=username.data).first():
            raise ValidationError("ESTE USUARIO JA CADASTRADO")


    def validate_email(self, email):
        if Cadastrar.query.filter_by(email=email.data).first():
            raise ValidationError("ESTE USUARIO JA CADASTRADO")
        


class ClienteLoginForm(FlaskForm):
    email= StringField('Email: ', [validators.DataRequired()])
    password = PasswordField,('Senha: ',[validators.DataRequired()])


