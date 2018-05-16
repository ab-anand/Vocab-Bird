from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.validators import (DataRequired, Email,
                               Length)

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', validators=[
                                        Email(),
                                        DataRequired(),
                                        Length(min=2),
                                        Length(max=50)
                                        ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
