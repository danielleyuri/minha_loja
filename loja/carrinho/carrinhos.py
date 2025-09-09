from flask import redirect, render_template, url_for, flash, request, session, current_app

from loja import app, db

from loja.produtos.models import Addproduto
from loja.produtos.rotas import marcas, categorias
import json


def M_Dicionarios(dic1, dic2):
    if isinstance(dic1, list) and isinstance(dic2, list):
        return dic1 + dic2
    elif isinstance(dic1, list) and isinstance(dic2, dict):
        return dict(list(dic1.tems()) + list(dic2.items()))
    return False

@app.route('/addcart', methods=['GET', 'POST'])
def AddCart():
    try:
        produto_id = request .form.get('produto_id')
        quantity = request .form.get('quantity')
        colors = request .form.get('colors')
        produto = Addproduto.query.filter_by(id=produto_id).first()

        if request.method =="POST":
            DictItems = {produto_id:{'Nome':produto.name, 'Preco':produto.price, 
                                    'Desconto':produto.discount,'Cor':produto.colors,
                                    'Quantidade':produto.quantity,'Image':produto.image_1, 
                                    'colors': produto.colors}}
            
            if 'LojaCarrinho' in session:
                print(session['LojainCarrinho'])
                if produto_id in session['LojainCarrinho']:
                    if produto_id in session['LojainCarrinho']:
                        for key, item in session['LojainCarrinho'].items():
                            if int(key) == int(produto_id):
                                session.modified = True
                                item['quantity']+=1

            else:
                session['LojainCarrinho'] = M_Dicionarios(session['LojainCarrinho'],DictItems)
                return redirect(request.referrer)
            
        else:
            session['LojainCarrinho'] = DictItems
            return redirect(request.referrer)
                

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)



@app.route('/carros')
def getCart():
    if 'LojainCarrrinho' not in session or len(session['LojainCarrinho']) <=0:
        return redirect(url_for('home'))
    subtotal = 0
    valorpagar = 0
    for key, produto in session['LojainCarrinho'].items():
            discount = (produto['discount']/100) * float(produto['price'])
            subtotal += float(produto['price']/100) * int(produto['quantity'])
            subtotal -= discount
            valorpagar = float("%.2f" %(1.06 * subtotal ))

    return render_template('produtos/carros.html', valorpagar=valorpagar, marcas=marcas(), categorias=categorias())



@app.route('/updateCarro/<int:code>', methods=["POST"])
def updateCarro(code):
    if 'LojainCarrrinho' not in session or len(session['LojainCarrinho'])<=0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code: 
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('ITEM ATUALIZADO')
                    return redirect(url_for('getCart'))


        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
        

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'LojainCarrrinho' not in session or len( session['LojainCarrinho'])<=0:
        return redirect(url_for('home'))
    
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
            if int(key) == id: 
                session['LojainCarrinho'].pop(key,None)
                flash('ITEM ATUALIZADO')
                return redirect(url_for('getCart'))


    except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
        


@app.route('/limparcarro')
def limparcarro(id):
    
    try:
        session.pop['LojainCarrinho',None]
        return redirect(url_for('home'))


    except Exception as e:
            print(e)
    
        
