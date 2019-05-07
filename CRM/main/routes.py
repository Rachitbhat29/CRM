from flask import render_template, url_for, flash, redirect, request
from CRM.models import User, Customer, Addresses
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    customers_data=Customer.query.order_by(Customer.cust_id.desc()).paginate(page=page ,per_page=2)
    return render_template('Home.html', posts= customers_data)
