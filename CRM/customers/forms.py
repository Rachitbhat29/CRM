from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length,Email,EqualTo, ValidationError

class CreateCustomerForm(FlaskForm):
    first_name = StringField('Firstname', validators=[DataRequired()])
    last_name = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators= [DataRequired()])
    submit = SubmitField('Create')
