from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import Required, Email, Length, DataRequired, NumberRange


class FactoryForm(FlaskForm):
    code = StringField('Factory Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Factory Code"})
    name = StringField('Factory Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Factory Name"})

class CollectionPerGrader(FlaskForm):
	grader = SelectField('Grader:', validators=[Required()], id='select grader',  coerce=int)
	start_date = StringField('Start Date:', validators=[Required()], id='datetimepicker1')
	end_date = StringField('End Date:', validators=[Required()], id='datetimepicker2')



