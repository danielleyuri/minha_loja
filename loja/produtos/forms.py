from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField



class Addprodutos(Form):
    name = StringField('Nome do produto',[validators.DataRequired()])
    price = StringField('preco',[validators.DataRequired()])
    discount = StringField('Desconto',[validators.DataRequired()])
    discription = TextAreaField('Descricao',[validators.DataRequired()])
    stock = IntegerField('estoque',[validators.DataRequired()])
    colors = TextAreaField('cor',[validators.DataRequired()])


    image_1 = FileField('Image 1 ', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('image 2 ', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Image 3 ', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])