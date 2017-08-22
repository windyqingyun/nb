from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,PasswordField
from wtforms.validators import Required, Length, Email, Regexp,equal_to
from wtforms import ValidationError


class LoginForm(FlaskForm):
	account = StringField('account',validators=[Required()])
	password = PasswordField('password',validators=[Required()])
	
	submit = SubmitField('login')
	#rsubmit = SubmitField('register')	

class RegisterForm(FlaskForm):
	account = StringField('account',validators=[Required()])
	password = PasswordField('password',validators=[Required(),equal_to('cpassword')])
	cpassword = PasswordField('comfirmPass')
	submit = SubmitField('register')

