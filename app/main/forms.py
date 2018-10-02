from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import Required, Email, Length, DataRequired, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename



class SeasonForm(FlaskForm):
    code = StringField('Season Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Season Code"})
    name = StringField('Season Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Season Name"})

class FactoryForm(FlaskForm):
    number = StringField('Factory Number', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Factory Number"})
    name = StringField('Factory Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Factory Name"})
    
class CooperativeForm(FlaskForm):
    code = StringField('Cooperative Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Cooperative Code"})
    name = StringField('Cooperative Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Cooperative Name"})

class SocietyForm(FlaskForm):
    code = StringField('Society Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Society Code"})
    name = StringField('Society Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Society Name"})
    cooperative = SelectField('Cooperative Union:', validators=[Required()], id='select_cooperative',  coerce=int)


class ProduceForm(FlaskForm):
    code = StringField('Produce Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Produce Code"})
    name = StringField('Produce Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Produce Name"})
    


class AdvanceForm(FlaskForm):
    amount = StringField('amount', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Amount"})



class LimitForm(FlaskForm):
    percentage = StringField('percentage', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Percentage"})

class LicenceForm(FlaskForm):
    start_date = StringField('Start Date:', validators=[Required()], id='datetimepicker1')
    end_date = StringField('End Date:', validators=[Required()], id='datetimepicker2')
   


class GroupForm(FlaskForm):
    code = StringField('Group Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Group Code"})
    name = StringField('Group Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Group Name"})

class ProcessorForm(FlaskForm):
    code = StringField('Processor Code', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Processor Code"})
    name = StringField('Processor Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Processor Name"})
    type = StringField('Processor Type', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Processor Type"})


class RouteForm(FlaskForm):
    name = StringField('Route Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Route Name"})
    start = StringField('Route Start', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Route start-point"})
    end = StringField('Route End', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Route end-point"})




class CentreForm(FlaskForm):
    name = StringField('Centre Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Centre Name"})
    route = SelectField('Route:', validators=[Required()], id='select_route',  coerce=int)


class FarmersForm(FlaskForm):
    supplier_no = StringField('Supplier No', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Supplier/Farmer No"})
    first_name = StringField('First Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Last Name"})
    id_number = StringField('ID No', validators=[Required()], render_kw={"placeholder": "National ID No"})
    phone_number = StringField('Phone Number', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Phone Number"})
    centre = SelectField('Centre:', validators=[Required()], id='select_centre',  coerce=int)



class FarmersUploadForm(FlaskForm):
    farmers_csv = FileField('farmers_csv', validators=[FileAllowed(['csv'], 'Upload CSV Files only!')])


class ContractForm(FlaskForm):
    produce = SelectField('Produce:', validators=[Required()], id='select_produce',  coerce=int)
    factory = SelectField('Factory:', validators=[Required()], id='select_factory',  coerce=int)
    price = StringField('Price', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Price per KG"})
    payment_term = SelectField(u'Payment Term', choices=[('WK', 'Weekly'), ('MN', 'Monthly'), ('DL', 'Daily')])


class VehicleForm(FlaskForm):
    reg_no = StringField('Reg No', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Reg No"})
    make = StringField('Model', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Make"})
    body = StringField('Vehicle Type', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Body"})
    color = StringField('Color', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Color"})
    ownership = SelectField(u'Ownership', choices=[('OWN', 'Owned'), ('HRD', 'Hired')])

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
    
class CollectionPerGrader(FlaskForm):
    grader = SelectField('Grader:', validators=[Required()], id='select grader',  coerce=int)
    start_date = StringField('Start Date:', validators=[Required()], id='datetimepicker1')
    end_date = StringField('End Date:', validators=[Required()], id='datetimepicker2')

class DriverForm(FlaskForm):
    first_name = StringField('First Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Last Name"})
    phone_number = StringField('Phone Number', validators=[Required(), Length(1,64)], render_kw={"placeholder": "Phone Number"})