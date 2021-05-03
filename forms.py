from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, TextAreaField
from wtforms.validators import DataRequired

from models import User


class UserForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(UserForm):
    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        user = User.get(login=self.login.data)

        valid = user and user.check_password(self.password.data)

        if not valid:
            self.password.errors.append('Wrong username or password')

        return valid


class RegisterForm(UserForm):
    first_name = StringField('First name', validators=[DataRequired()])

    def validate(self):
        if not super(RegisterForm, self).validate():
            return False

        return not User.get(login=self.login.data)


class MessageForm(FlaskForm):
    text = TextAreaField('Message', validators=[DataRequired()])


class ProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('First name', validators=[DataRequired()])
