import os
import secrets
from PIL import Image
from flask import url_for, current_app
from CRM import  db, bcrypt, mail
from CRM.models import User
from flask_mail import Message

def save_picture(picture_data):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(picture_data.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(picture_data)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


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