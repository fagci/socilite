from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
from models import User


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        try:
            possible_user = User.get(login=self.login.data)
        except:
            possible_user = None

        valid = possible_user and possible_user.check_password(
            self.password.data)

        if not valid:
            self.password.errors.append(
                'Wrong username or password or user not found')
        return valid


class RegisterForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate(self):
        if not super(RegisterForm, self).validate():
            return False

        try:
            return not User.get(login=self.login.data)
        except:
            return True
