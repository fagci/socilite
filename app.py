#!/usr/bin/env python

from datetime import datetime
from forms import LoginForm, RegisterForm

from flask import Flask, flash, redirect, render_template, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from pony.flask import Pony
from pony.orm.core import flush

from models import Message, User, db

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='my_$3cr37',
    PONY={
        'provider': 'sqlite',
        'filename': 'db.sqlite',
        'create_db': True
    }
))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        possible_user = User.get(login=form.login.data)
        possible_user.last_login = datetime.now()
        login_user(possible_user)
        return redirect('/')

    return render_template('login.html', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            login=form.login.data,
            password=form.password.data,
            first_name=form.first_name.data
        )
        user.last_login = datetime.now()
        flush()
        login_user(user)
        return redirect('/')
    return render_template('reg.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html', messages=current_user.messages)


if __name__ == '__main__':
    db.bind(**app.config['PONY'])
    db.generate_mapping(create_tables=True)
    Pony(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(id=user_id)
    app.run()
