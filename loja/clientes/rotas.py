from flask import redirect, render_template, url_for, flash, request, session,current_app 
from flask_bcrypt import Bcrypt
from .forms import CadastroClienteForm, ClienteLoginForm

from loja import db, app, photos, bcrypt, login_manager
import secrets
import os
from .models import Cadastrar, ClientePedido
from flask_login import login_required, current_user, login_user, logout_user




@app.route('/cliente/cadastrar', methods=['GET','POST'])
def cadastrar_clientes():
    form = CadastroClienteForm(request.form)
    if form.validate_on_submit():

        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data, username=form.username.data, email=form.email.data,
        password=hash_password, country=form.country.data, city=form.city.data, contact=form.contact, 
        address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(cadastrar)
        flash(f'OBRIGADO {form.name.date} POR CADASTRAR', 'success')
        db.session.commit()
        return redirect(url_for('login'))   
    return render_template('cliente/cliente.html', form=form)



@app.route('/cliente/login', methods=['GET','POST'])
def clienteLogin():
    form = ClienteLoginForm
    if form.validate_on_submit():
        user = Cadastrar.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Login efetuado', 'success')
            next=request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'senha e email incorretos', 'danger')
        return redirect(url_for(clienteLogin))
    
    return render_template('cliente/login.html', form=form)


@app.route('/cliente/logout')
def cliente_logout():
    logout_user()

    return redirect(url_for('home'))



@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        try:
            p_order =  ClientePedido(notafiscal=notafiscal, cliente_id=cliente_id, pedido=session['LojainCarrinho'])
            db.sesion.add(p_order)
            db.sesion.commit()
            session.pop('LojainCarrinho')

            flash(f'seu pedido foi concluido com sucesso', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            print(e)
            flash(f'nao foi possivel processar o seu pedido', 'danger')
            return redirect(url_for('getCart'))


 


