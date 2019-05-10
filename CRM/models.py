from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from CRM import db,login_manager
from flask import current_app
from flask_login import UserMixin
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def get_reset_token(self, expires_sec=20):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def  __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}')"

class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(20), unique=True, nullable =False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Addresses', backref = 'customerdata', lazy= True)

    def  __repr__(self):
        return f"('{self.first_name}','{self.last_name}','{self.email}','{self.cust_id}')"



class Addresses(db.Model):
    cust_id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.Text, nullable= True)
    date_posted = db.Column(db.DateTime, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable= False)

    def  __repr__(self):
        return f"Addresses(''{self.address}','{self.date_posted}','{self.customer_id}')"