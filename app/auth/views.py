from flask import render_template, flash, redirect, url_for, request
from . import auth
from .forms import LoginForm
from ..models import User, Licence
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from .. import db

@auth.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('.login'))
        if(check_licence(user)):
            login_user(user)
        else:
            flash('Licence Expired. Kindly Contact System Admin', 'error')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('.login'))

def check_licence(user):
    try:
        if user.role_id == 3:
            return True
        else:  
            licence = Licence.query.filter_by(status=True).first()
            if (licence):
                if(datetime.now() > licence.end_date):
                    licence.status = False
                    db.session.commit()
                    return False
                else:
                    return True
            else:
                return False
    except:
        return False
