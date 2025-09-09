from flask import redirect, render_template, url_for, flash, request, session,current_app 
from flask_bcrypt import Bcrypt
from .forms import CadastroClienteForm
from loja import db, app, photos, bcrypt
import secrets
import os
from .model import Cadastrar



@app.route('/cliente/cadastrar', methods=['GET','POST'])
def cadastrar_clientes():
    form = CadastroClienteForm(request.form)
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data, username=form.username.data, email=form.email.data,
        password=hash_password, country=form.country.data, city=form.city.data, contact=form.contact, address=form.address.data,
        zipcode=form.zipcode.data)
        db.session.add(cadastrar)
        flash(f'OBRIGADO {form.name.date} POR CADASTRAR', 'success')
        db.session.commit()
        return redirect(url_for('login'))   
    return render_template('cliente/cliente.html', form=form)



