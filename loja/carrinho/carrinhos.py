from flask import redirect, render_template, url_for, flash, request, session,current_app

from loja import app, db

from loja.produtos.models import Addproduto
from loja.produtos.rotas import marca, categoria


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

        if produto_id and quantity and colors and request.method =="POST":
            DictItems = {produto_id:{'Nome':produto.name, 'Preco':produto.price, 'Desconto':produto.discount,'Cor':produto.colors,'Quantidade':produto.quantity,'Image':produto.image_1,}}
            if 'LojaCarrinho' in session:
                print(session['LojainCarrinho'])
                if produto_id in session['LojainCarrinho']:
                    print("Produto ja adicionado no carrinho")

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
    if'LojainCarrinho' not in session:
        return redirect(request.referrer)
    return render_template('produtos/carros.html')