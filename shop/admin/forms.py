from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import Email


class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginFrom(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), Email()])
    password = PasswordField('New Password', [
        validators.DataRequired()])
