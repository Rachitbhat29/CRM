from flask import render_template, url_for, flash, redirect
from CRM import app
from CRM.forms import RegistrationForm,LoginForm
from CRM.models import Customer,Addresses

customers_date = [
    {
        'cust_id': '1',
        'First_name': 'John',
        'Last_name': 'M',
        'Address': '123 Washington'
    },
    {
        'cust_id' : '2',
        'First_name' : 'Ron',
        'Last_name' : 'K',
        'Address' : '321 Newyork'
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template('Home.html', posts= customers_date)

@app.route("/register", methods= ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title = 'Register', form= form)

@app.route("/login", methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abc@xyz.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsucessful attempt. Please chec username or password', 'danger')
    return render_template('login.html',title = 'Login', form= form)