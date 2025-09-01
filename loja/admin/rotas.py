from flask import render_template,  session, request, url_for, flash, redirect
from wtforms.validators import Email
from loja.produtos.models import Addproduto, Marca, Categoria

from loja import app, db, bcrypt

from .forms import RegistrationForm
from .forms import LoginFormulario
from .models import User
import os


@app.route('/admin')
def admin():
    if'email' not in session:
        flash(f'Inicie o seu login', 'secondary')
        return redirect(url_for('login'))
    produtos = Addproduto.query.all()
    return render_template ('admin/index.html', title='pagina administrativa', produtos=produtos)


@app.route('/marca')
def marca():
    if'email' not in session:
        flash(f'Iniciar o seu primeiro login', 'secondary')
        return redirect(url_for('login'))
    marca = Marca.query.order_by(Marca.id.desc()).all()
    return render_template ('admin/marca.html', title='Marca', marca=marca)



@app.route('/categoria')
def categoria():
    if'email' not in session:
        flash(f'Iniciar o seu primeiro login', 'secondary')
        return redirect(url_for('login'))
    categorias = Categoria.query.order_by(Categoria.id.desc()).all()
    return render_template ('admin/marca.html', title='Categorias', categorias=categorias)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():

        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigada {form.name.data} por Registrar', 'secondary')

        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title="Pagina para Registros")


@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginFormulario(request.form)
    if request.method == "POST" and form.validate():
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'ola {form.email.data} seja bem-vindo', 'secondary')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'NAO FOI possivel concluir o login.')
    return render_template ('admin/login.html', form=form, title='pagina login')