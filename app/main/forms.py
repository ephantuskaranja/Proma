from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import Required, Email, Length, DataRequired, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename


class SeasonForm(FlaskForm):
    code = StringField('Season Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Season Code"})
    name = StringField('Season Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Season Name"})

class FactoryForm(FlaskForm):
    code = StringField('Factory Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Factory Code"})
    name = StringField('Factory Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Factory Name"})

class ProduceForm(FlaskForm):
    code = StringField('Produce Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Produce Code"})
    name = StringField('Produce Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Produce Name"})
    cess = StringField('KDB Cess', validators=[Required()], render_kw={"placeholder": "Kenya Dairy Board Cess"})


class GroupForm(FlaskForm):
    code = StringField('Group Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Group Code"})
    name = StringField('Group Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Group Name"})

class ProcessorForm(FlaskForm):
    code = StringField('Processor Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Processor Code"})
    name = StringField('Processor Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Processor Name"})


class RouteForm(FlaskForm):
    code = StringField('Route Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Route Code"})
    name = StringField('Route Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Route Name"})


class CentreForm(FlaskForm):
    code = StringField('Centre Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Centre Code"})
    name = StringField('Centre Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Centre Name"})
    route = SelectField('Route:', validators=[Required()], id='select_route',  coerce=int)


class FarmersForm(FlaskForm):
    supplier_no = StringField('Supplier No', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Supplier/Farmer No"})
    first_name = StringField('First Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Last Name"})
    id_number = StringField('ID No', validators=[Required()], render_kw={"placeholder": "National ID No"})
    phone_number = StringField('Phone Number', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Phone Number"})
    centre = SelectField('Station:', validators=[Required()], id='select_station',  coerce=int)
    group = SelectField('Group:', validators=[Required()], id='select_group',  coerce=int)


class FarmersUploadForm(FlaskForm):
    farmers_csv = FileField('farmers_csv', validators=[FileAllowed(['csv'], 'Upload CSV Files only!')])


class ContractForm(FlaskForm):
    produce = SelectField('Produce:', validators=[Required()], id='select_produce',  coerce=int)
    factory = SelectField('Factory:', validators=[Required()], id='select_factory',  coerce=int)
    price = StringField('Price', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Price per KG"})
    payment_term = SelectField(u'Payment Term', choices=[('WK', 'Weekly'), ('MN', 'Monthly'), ('DL', 'Daily')])


class VehicleForm(FlaskForm):
    reg_no = StringField('Reg No', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Reg No"})
    make = StringField('Make', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Make"})
    body = StringField('Body', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Body"})
    color = StringField('Color', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Color"})
    ownership = SelectField(u'Ownership', choices=[('LNG', 'Longisa'), ('HRD', 'Hired')])

class GraderForm(FlaskForm):
    first_name = StringField('First Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Last Name"})
    phone_number = StringField('Phone Number', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Phone Number"})
    contract_price = StringField('Contarct Price', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Contract Price"})
    app_username = StringField('App Username', validators=[Required(), Length(1,64)], render_kw={"placeholder": "App Username"})
    app_password = StringField('App Password', validators=[Required(), Length(1,64)], render_kw={"placeholder": "App Password"})
    role = SelectField('Role:', validators=[Required()], id='select Role',  coerce=int)

class TripForm(FlaskForm):
    trip_date = StringField('Trip Date:', validators=[Required()], id='datetimepicker1')
    route = SelectField('Route:', validators=[Required()], id='select route',  coerce=int)
    grader = SelectField('Grader:', validators=[Required()], id='select grader',  coerce=int)
    driver = SelectField('Driver:', validators=[Required()], id='select driver',  coerce=int)
    vehicle = SelectField('Vehicle:', validators=[Required()], id='select vehicle',  coerce=int)
    


class CompleteTripForm(FlaskForm):
     total_weight_received = StringField('Total Kgs Received', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Total Kgs Received at the factory"})
    


class DriverForm(FlaskForm):
    first_name = StringField('First Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Last Name"})
    phone_number = StringField('Phone Number', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Phone Number"})