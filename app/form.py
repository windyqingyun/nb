from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Length, equal_to


class LoginForm(FlaskForm):
    account = StringField('account', validators=[Required(), Length(min=6,max=20)])
    password = PasswordField('password', validators=[Required(), Length(min=6,max=20)])
    submit = SubmitField('login')


class RegisterForm(FlaskForm):
    account = StringField('account', validators=[Required(), Length(min=6,max=20)])
    password = PasswordField('password', validators=[Required(), Length(min=6,max=20) ,equal_to('cpassword')])
    cpassword = PasswordField('comfirmPass')
    submit = SubmitField('register')

