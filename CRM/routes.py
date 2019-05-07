import os
import secrets
import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from CRM import app, db, bcrypt, mail
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






