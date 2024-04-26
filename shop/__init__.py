from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
'''
Run this to correct any error from flask_uploads
pip install git+https://github.com/jugmac00/flask-reuploaded@53234dd
'''


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.app_context().push()
app. config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'uhlvvwviwbvqwhhdqhdhdg'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from shop.admin import routes
from shop.products import routes
from shop.carts import carts


 