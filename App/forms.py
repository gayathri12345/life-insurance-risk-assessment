from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired(),Length(min=4,max=15)])
    password=PasswordField('Password',validators=[InputRequired(), Length(min=4,max=80)])


class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired(),Length(min=4,max=15)])
    email=StringField("Email" ,validators=[InputRequired(), Email(message='Invalid email'), Length(min=5,max=15)])
    password=PasswordField('Password',validators=[InputRequired(), Length(min=4,max=80)])


class UploadForm(FlaskForm):
    file=FileField()