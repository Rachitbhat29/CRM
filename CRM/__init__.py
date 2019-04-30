from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY']= '818a3da9a9af6c628fbe9e5e0c6e9815'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= 'True'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from CRM import route