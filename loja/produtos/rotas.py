from loja.admin.rotas import categorias, marcas
from flask import redirect, render_template, url_for, flash, request, session,current_app 
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto
import secrets, os


def marcas():
        marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
        return marcas


def categorias():
        categorias = Marca.query.join(Addproduto, (Categoria.id == Addproduto.marca_id)).all()
        return categorias



@app.route('/')
def home():
    pagina = request.args.get('pagina',1, type=int)
    produtos = Addproduto.query.filter(Addproduto.stock > 0).order_by(Addproduto.id.desc()).paginate(page=pagina, per_page=3)
    return render_template('produtos/index.html', produtos=produtos, marcas=marcas, categorias=categorias)



@app.route('/search', methods=['GET','POST'])
def search():
     
    if request.method=="POST":
        form= request.form
        search_value = form['search_string']
        search="%{0}%".format(search_value)
        produtos = Addproduto.query.filter(Addproduto.name.like(search)).all()
        return render_template('pesquisar.html', produtos=produtos, marcas=marcas, categorias=categorias)
    else:
        return redirect('/')


@app.route('/pesquisar')
def pesquisar():
     searchword = request.args.get('q')
     produtos=Addproduto.query.msearch(searchword, fields=['name', 'desc'], limit=3)
     return render_template('produtos/pesquisar.html', produtos=produtos)



@app.route('/marca/<int:id>')
def get_marca(id): 
    get_m = Marca.query.filter_by(id=id).first_or_404()
    pagina = request.args.get('pagina',1, type=int)
    marca = Addproduto.query.filter_by(marca=get_m).paginate(page=pagina, per_page=3)
    return render_template('/produtos/index.html', marca=marca, marcas=marcas(), categorias=categorias(), get_m=get_m)


@app.route('/produto/<int:id>')
def pagina_unica(id): 
    produto = Addproduto.query.get_or_404(id)

    return render_template('/produtos/pagina_unica.html', produto=produto, marcas=marcas(), categorias=categorias())



@app.route('/categorias/<int:id>')
def get_categoria(id):
    pagina = request.args.get('pagina',1, type=int)
    get_cat = Categoria.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduto.query.filter_by(categoria=get_cat).paginate(page=pagina, per_page=3)

    return render_template('/produtos/index.html',get_cat_prod=get_cat_prod , categorias=categorias(), marcas=marcas(), get_cat=get_cat)



@app.route('/addmarca', methods=['GET','POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Iniciar o seu primeiro login', 'secondary')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marca(name=getmarca)
        db.session.add(marca)
        flash(f'a marca {getmarca} foi adicionada com sucesso', 'secondary')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marca='marcas')



@app.route('/updatemarca/<int:id>', methods=['GET','POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Iniciar o seu primeiro login', 'secondary')
        return redirect(url_for('login'))
    
    updatemarca= Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method=='POST':
        updatemarca.name = marca
        flash(f'fabricante foi atualizado com sucasso', 'secondary')
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template('/produtos/updatemarca.html', title='Atualizar fabricantes', updatemarca=updatemarca)



@app.route('/deletemarca/<int:id>', methods=['POST'])
def deletemarca(id):
    marca= Marca.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(marca)
        db.session.commit()        
        flash(f'A marca {marca.name} FOI DELETADA COM SUCESSO', 'secondary')
        return redirect(url_for('admin'))
    flash(f'A marca {marca.name} NAO FOI DELETADA', 'warning')
    return redirect(url_for('admin'))



@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
            flash(f'Iniciar o seu primeiro login', 'secondary')
            return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('categoria')
        categoria = Categoria(name=getmarca)
        db.session.add(categoria)
        flash(f'a categoria {getmarca} foi adicionada com sucesso', 'secondary')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('/produtos/addmarca.html')



@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Iniciar o seu primeiro login', 'secondary')
        return redirect(url_for('login'))
    
    updatecat= Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')

    if request.method=='POST':
        updatecat.name = categoria
        flash(f'categoria foi atualizado com sucasso', 'secondary')
        db.session.commit()
        return redirect(url_for('categoria'))

    return render_template('/produtos/updatemarca.html', title='Atualizar fabricantes', updatecat=updatecat)


@app.route('/deletecategoria/<int:id>', methods=['POST'])
def deletecategoria(id):
   
    categoria= Categoria.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(categoria)
        db.session.commit()        
        flash(f'A categoria {categoria.name} FOI DELETADA COM SUCESSO', 'secondary')
        return redirect(url_for('admin'))
    flash(f'A categoria {categoria.name} NAO FOI DELETADA', 'warning')
    return redirect(url_for('admin'))


@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if 'email' not in session:
            flash(f'Iniciar o seu primeiro login', 'secondary')
            return redirect(url_for('login'))
    
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)
    if request.method=="POST":
        
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")                   

        addproduto = Addprodutos(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc, marca_id=marca, categoria_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3)

        db.session.add(addproduto)
        flash(f'a produto {name} foi adicionada com sucesso', 'secondary')
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template('/produtos/addproduto.html', title='Adicionar produtos',form=form, marca=marcas, categoria=categorias)


@app.route('/updateproduto/<int:id>', methods=['GET','POST'])
def updateproduto(id):
        marca = Marca.query.all()
        categoria = Categoria.query.all()
        produto = Addprodutos.query.get_or_404(id)
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')
        form = Addprodutos(request.form)  

        if request.method=="POST":
            produto.name = form.name.data
            produto.price = form.price.data 
            produto.discount = form.discount.data

            produto.marca_id = marca
            produto.categoria_id = categoria

            produto.stock = form.stock.data
            produto.colors = form.colors.data
            produto.desc = form.discription.data

            if request.files.get('image_1'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images" + produto.image_1 ))            
                    produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

                except:
                    produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")


            if request.files.get('image_2'):
                try:

                    os.unlink(os.path.join(current_app.root_path, "static/images" + produto.image_2 ))            
                    produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

                except:
                    produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")


            if request.files.get('image_3'):
                try:

                    os.unlink(os.path.join(current_app.root_path, "static/images" + produto.image_3 ))            
                    produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

                except:
                    produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

            db.session.commit()
            flash(f'O produto foi atualizado com sucesso', 'secondary')
            return redirect(url_for('admin'))

        form.name.data = produto.name
        form.price.data = produto.price
        form.discount.data = produto.discount

        form.stock.data = produto.stock
        form.colors.data = produto.colors
        form.discription.data = produto.desc

        return render_template('/produtos/updateproduto.html', title='Atualizar produto', form=form, marcas=marca, categorias=categoria,produto=produto)


@app.route('/deleteproduto/<int:id>', methods=['POST'])
def deleteproduto(id):
   
    produto= Addprodutos.query.get_or_404(id)
    if request.method=='POST':
            if request.files.get('image_1'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images" + produto.image_1 ))            
                    os.unlink(os.path.join(current_app.root_path, "static/images" + produto.image_2 ))            
                    os.unlink(os.path.join(current_app.root_path, "static/images" + produto.image_3 ))      

                except Exception as e:
                    print(e)      

            db.session.delete(produto)
            db.session.commit()
            return redirect(url_for('admin'))
    flash(f'a produto {produto.name} foi apagado com sucesso', 'secondary')
    return redirect(url_for('admin'))


