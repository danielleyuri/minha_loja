from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators, PasswordField
from flask_wtf.file import FileField,FileRequired, FileAllowed





class CadastroClienteForm(Form):
    name = StringField('Nome: ')
    username = StringField('Usuario: ',[validators.DataRequired()])
    email= StringField('Email: ', [validators.DataRequired()])
    password = PasswordField,('Senha: ',[validators.DataRequired()])
    confirm = PasswordField('Digite novamente sua senha: ',[validators.DataRequired()])
    country = StringField('País: ',[validators.DataRequired()])
    state = StringField('Estado: ',[validators.DataRequired()])
    city = StringField('Cidade: ',[validators.DataRequired()])
    contact = StringField('Contato: ', [validators.DataRequired()])
    address = StringField('Endereço: ', [validators.DataRequired()])
    zipcode = StringField('Caixa-Postal: ', [validators.DataRequired()])
    profile = FileField('Pefil', validators=[FileAllowed('jpg','png','gif', 'jpeg'), 'Apenas fotos'])


    submit = SubmitField('Cadastrar')