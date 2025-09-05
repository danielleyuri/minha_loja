from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

from flask_bcrypt import Bcrypt
import os
from flask_msearch import Search 



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhaloja.db'
app.config['SECRET_KEY'] = 'livhreknbre564lijhclewjkhciluewhc'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


search = Search()
search.init_app(app)


from loja.admin import rotas
from loja.produtos import rotas
from loja.carrinho import carrinhos