import datetime
from flask import render_template, url_for, flash, redirect, request, jsonify
from CRM import  db
from CRM.customers.forms import CreateCustomerForm
from CRM.models import User,Customer,Addresses
from flask_login import login_user, current_user, logout_user, login_required
from flask import Blueprint
import json

customers = Blueprint('customers', __name__)


@customers.route("/eCRM/new_customer", methods= ['GET','POST'])
@login_required
def new_customer():
    form = CreateCustomerForm()
    if form.validate_on_submit():
        customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        db.session.add(customer)
        customer_data = Customer.query.filter_by(first_name = form.first_name.data, last_name=form.last_name.data, email= form.email.data).first()
        address = Addresses(address=form.address.data,date_posted= datetime.datetime.now(),cust_id=customer_data.cust_id, customer_id=customer_data.cust_id)
        db.session.add(address)
        db.session.commit()
        flash('Customer has been created','success')
        return redirect(url_for('main.home'))
    return render_template('create_customer.html', title='New Customer', form = form)


@customers.route("/customer/<int:cust_id>" , methods= ['GET','POST'])
@login_required
def open_customer(cust_id):
    cust = Customer.query.get_or_404(int(cust_id))
    address = Addresses.query.get_or_404(cust_id)
    return render_template('customer.html', post=cust)


@customers.route("/customer/<int:cust_id>/update", methods= ['GET','POST'])
@login_required
def update_customer(cust_id):
    customer = Customer.query.get_or_404(int(cust_id))
    address = Addresses.query.get_or_404(int(cust_id))
    form = CreateCustomerForm()
    if form.validate_on_submit():
        customer.first_name=form.first_name.data
        customer.last_name=form.last_name.data
        customer.email=form.email.data
        address.address=form.address.data
        db.session.commit()
        flash('Customer info has been udpated!', 'success')
        return render_template('customer.html', post=customer)
    elif request.method == 'GET':
        form.first_name.data = customer.first_name
        form.last_name.data =customer.last_name
        form.email.data = customer.email
        form.address.data = address.address
        form.submit.label.text='Update'
    return render_template('update_customer.html', title='Update Customer', form=form, legend= 'Update Customer', post= customer)


@customers.route("/customer/<int:cust_id>/delete", methods= ['POST'])
@login_required
def delete_customer(cust_id):
    customer = Customer.query.get_or_404(int(cust_id))
    address = Addresses.query.get_or_404(int(cust_id))
    db.session.delete(customer)
    db.session.delete(address)
    db.session.commit()
    flash('Customer has been deleted!','success')
    return redirect(url_for('main.home'))



@customers.route("/customer", methods= ['POST'])
def add_customers_api():
    customer = Customer(first_name=request.json['first_name'], last_name=request.json['last_name'], email=request.json['email'])
    db.session.add(customer)
    db.session.commit()
    #c = Customer.query.filter_by(first_name=request.json['first_name'], last_name=request.json['last_name'], email= request.json['email']).first()

    return jsonify({"first_name": request.json['first_name'],
                   "last_name" : request.json['last_name'],
                   "email" : request.json['email']})

@customers.route("/customer/no./<int:cust_id>", methods= ['GET'])
def get_customers_api(cust_id):
    customer = Customer.query.get_or_404(cust_id)
    #c = Customer.query.filter_by(first_name=request.json['first_name'], last_name=request.json['last_name'], email= request.json['email']).first()

    return jsonify({"first_name": customer.first_name,
                   "last_name" : customer.last_name,
                   "email" : customer.email})