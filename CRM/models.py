from CRM import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def  __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}')"

class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(20), unique=True, nullable =False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Addresses', backref = 'customerdata', lazy= True)

    def  __repr__(self):
        return f"Customer('{self.first_name}','{self.last_name}','{self.image_file}')"

class Addresses(db.Model):
    cust_id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.Text, nullable= True)
    date_posted = db.Column(db.DateTime, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable= False)

    def  __repr__(self):
        return f"Addresses(''{self.address}','{self.date_posted}','{self.customer_id}')"