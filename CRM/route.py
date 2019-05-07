import os
import secrets
import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from CRM import app, db, bcrypt, mail
from CRM.forms import (RegistrationForm,LoginForm, UpdateAccountForm, CreateCustomerForm,
                       RequestResetForm, ResetPasswordForm)
from CRM.models import User,Customer,Addresses
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

"""
customers_data = [
    {
        'cust_id': '1',
        'first_name': 'John',
        'last_name': 'M',
        'email': 'abc@a.com',
        'Address': '123 Washington'
    },
    {
        'cust_id' : '2',
        'first_name' : 'Ron',
        'last_name' : 'K',
        'email': 'bcd@b.com',
        'Address' : '321 Newyork'
    }

]"""

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    customers_data=Customer.query.order_by(Customer.cust_id.desc()).paginate(page=page ,per_page=2)
    return render_template('Home.html', posts= customers_data)

@app.route("/register", methods= ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',title = 'Register', form= form)

@app.route("/login", methods= ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsucessful attempt. Please chec username or password', 'danger')
    return render_template('login.html',title = 'Login', form= form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(picture_data):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(picture_data.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(picture_data)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods= ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file= image_file, form=form)


@app.route("/eCRM/new_customer", methods= ['GET','POST'])
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
        return redirect(url_for('home'))
    return render_template('create_customer.html', title='New Customer', form = form)


@app.route("/customer/<int:cust_id>" , methods= ['GET','POST'])
@login_required
def open_customer(cust_id):
    cust = Customer.query.get_or_404(int(cust_id))
    address = Addresses.query.get_or_404(cust_id)
    return render_template('customer.html', post=cust)


@app.route("/customer/<int:cust_id>/update", methods= ['GET','POST'])
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


@app.route("/customer/<int:cust_id>/delete", methods= ['POST'])
@login_required
def delete_customer(cust_id):
    customer = Customer.query.get_or_404(int(cust_id))
    address = Addresses.query.get_or_404(int(cust_id))
    db.session.delete(customer)
    db.session.delete(address)
    db.session.commit()
    flash('Customer has been deleted!','success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token = User.get_reset_token(user)
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset the password, visit the following link:
{url_for('reset_token', token = token, _external=True)}

If you did not make this request then simply ignore this email and no change will be made.
'''

    mail.send(msg)

@app.route("/reset_password", methods= ['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instructions to reset your password.','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods= ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is invalid or expired token!','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('You password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)