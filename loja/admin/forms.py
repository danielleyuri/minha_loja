from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField('Nome', [validators.Length(min=4, max=25)])
    username = StringField('Usuario', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Senha', [
        validators.DataRequired(),
        validators.EqualTo
    ])
    confirm = PasswordField('Digite a Senha Novamente')


class LoginFormulario(Form):
        email = StringField('Email', [validators.Length(min=6, max=35)])
        password = PasswordField('Senha', [ validators.DataRequired()])