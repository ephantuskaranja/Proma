from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Username", "aria-describedby": "helpBlock2"})
	password = PasswordField('Password', validators=[Required()], render_kw={"placeholder": "Password", "aria-describedby": "helpBlock3"})
	remember_me = BooleanField('Keep me logged in')