from flask import render_template, flash, redirect, url_for, request
from . import auth
from .forms import LoginForm
from ..models import User
from flask_login import login_user, logout_user, login_required


@auth.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('.login'))  
        login_user(user)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('.login'))

