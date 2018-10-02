from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    app_users = db.relationship('AppUser', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(150))
    user_pin = db.Column(db.String(10))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(128))
    factories = db.relationship('Factory', lazy='dynamic', backref='creator')
    cooperative = db.relationship('Cooperative', lazy='dynamic', backref='creator')
    society = db.relationship('Society', lazy='dynamic', backref='creator')
    groups = db.relationship('Group', lazy='dynamic', backref='creator')
    processors = db.relationship('Processor', lazy='dynamic', backref='creator')
    produce = db.relationship('Produce', lazy='dynamic', backref='creator')
    route = db.relationship('Route', lazy='dynamic', backref='creator')
    grader_payments = db.relationship('GraderPayment', lazy='dynamic', backref='creator')
    farmers = db.relationship('Farmer', lazy='dynamic', backref='creator')
    seasons = db.relationship('Season', lazy='dynamic', backref='creator')
    vehicles = db.relationship('Vehicle', lazy='dynamic', backref='creator')
    app_users = db.relationship('AppUser', lazy='dynamic', backref='creator')
    drivers = db.relationship('Driver', lazy='dynamic', backref='creator')
    trips_creator = db.relationship('Trip', lazy='dynamic', backref='trips_creator')
    trips_updater = db.relationship('Trip', lazy='dynamic', backref='trips_updater')
    collection_centres = db.relationship('CollectionCentre', lazy='dynamic', backref='collection_centres_creator')
    farmer_advance = db.relationship('FarmerAdvance', lazy='dynamic', backref='creator')
    advance = db.relationship('Advance', lazy='dynamic', backref='creator')
    licence = db.relationship('Licence', lazy='dynamic', backref='creator')

   
    form_excluded_columns = ('password_hash')

    def to_json(self):
        return {
            'username':self.username,
            'name':self.name,
            'user_pin':self.user_pin,
            'role_id':2,
        }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class Factory(db.Model):
    __tablename__ = 'factories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    number = db.Column(db.String(10), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)


    def to_json(self):
        return {
            'number':self.number,
            'name':self.name,
        }



    def __repr__(self):
        return self.name


class Cooperative(db.Model):
    __tablename__ = 'cooperative'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    society = db.relationship('Society', lazy='dynamic', backref='cooperative')


    # def to_json(self):
    #     return {
    #         'code':self.code,
    #         'name':self.name,
    #     }


    # def __repr__(self):
    #     return self.name

class Society(db.Model):
    __tablename__ = 'society'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    cooperative_id = db.Column(db.Integer, db.ForeignKey('cooperative.id'))


    # def to_json(self):
    #     return {
    #         'code':self.code,
    #         'name':self.name,
    #     }


    # def __repr__(self):
    #     return self.name


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    # farmers = db.relationship('Farmer', lazy='dynamic', backref='group')


    def __repr__(self):
        return self.name


class Processor(db.Model):
    __tablename__ = 'processors'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    type = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)


    def __repr__(self):
        return self.name



class Produce(db.Model):
    __tablename__ = 'produce'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    produce = db.relationship('Collection', lazy='dynamic', backref='farmer_produce')
    contract = db.relationship('FarmerContract', lazy='dynamic', backref='produce')

    def to_json(self):
        return {
            'code':self.code,
            'name':self.name
        }



    def __repr__(self):
        return self.name


class Advance(db.Model):
    __tablename__ = 'advance'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Float, default=0.0)
    # produce = db.relationship('Collection', lazy='dynamic', backref='farmer_produce')
    

    # def to_json(self):
    #     return {
    #         'code':self.code,
    #         'name':self.name
    #     }



    # def __repr__(self):
    #     return self.name


class LoanLimit(db.Model):
    __tablename__ = 'limits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    percentage = db.Column(db.Float, default=0.0)



class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(10), unique=True, index=True)
    make = db.Column(db.String(64))
    body = db.Column(db.String(64))
    color = db.Column(db.String(64))
    ownership = db.Column(db.String(5))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    trips = db.relationship('Trip', lazy='dynamic', backref='vehicle')


    def to_json(self):
        return {
            'vehicle_id':self.id,
            'name':self.reg_no
        }



    def __repr__(self):
        return self.reg_no

class AppUser(db.Model):
    __tablename__ = 'app_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(20), unique=True, index=True)
    contract_price = db.Column(db.String(20), unique=True, index=True)
    app_password = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    trips = db.relationship('Trip', lazy='dynamic', backref='grader')


    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)


    def __repr__(self):
        return self.fullname


    def to_json(self):
        return {
            'grader_id':self.id,
            'username':self.username,
            'name':self.fullname,
            'user_pin':self.app_password,
            'role_id':self.role_id,
        }



class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(20), unique=True, index=True)
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trips = db.relationship('Trip', lazy='dynamic', backref='driver')

    def to_json(self):
        return {
            'driver_id':self.id,
            'name':self.fullname
        }

    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)


    def __repr__(self):
        return self.fullname



class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    start = db.Column(db.String(64), index=True)
    end = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    trips = db.relationship('Trip', lazy='dynamic', backref='route')
    centres = db.relationship('CollectionCentre', lazy='dynamic', backref='route')

    def to_json(self):
        return {
            'route_id': self.id,
            'name':self.name,
            'start':self.start,
            'end':self.end
        }



    def __repr__(self):
        return self.name

class CollectionCentre(db.Model):
    __tablename__ = 'collection_centres'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    farmers = db.relationship('Farmer', lazy='dynamic', backref='farmer')


    def to_json(self):
        return {
            'code':self.code,
            'name':self.name,
            'factory_code': self.code,
            'centre_id' : self.id
        }



    def __repr__(self):
        return self.name


class Farmer(db.Model):
    __tablename__ = 'farmers'
    id = db.Column(db.Integer, primary_key=True)
    supplier_no = db.Column(db.String(20), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    id_number = db.Column(db.Integer)
    phone_number = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    centre_id = db.Column(db.Integer, db.ForeignKey('collection_centres.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    collections = db.relationship('Collection', lazy='dynamic', backref='collection')
    contracts = db.relationship('FarmerContract', lazy='dynamic', backref='farmer')
    payments = db.relationship('TripPayment', lazy='dynamic', backref='farmer')


    def get_cumm_weight(self):
        cum_weight = 0
        collections = Collection.query.filter_by(farmer_id=self.id)
        for col in collections:
            cum_weight = cum_weight + col.produce_weight
        return cum_weight

    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)


    def to_json(self):
        return {
            'supplier_no':self.supplier_no,
            'name':self.first_name + " " + self.last_name,
            'cum_weight':self.get_cumm_weight(),
            'centre_id':self.centre_id
        }

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), index=True)
    total_weight_collected = db.Column(db.Float, default=0.0)
    total_weight_received = db.Column(db.Float, default=0.0)
    grader_payment = db.Column(db.Float, default=0.0)
    payment_grader_status = db.Column(db.Boolean, default=False)
    payment_generated = db.Column(db.Boolean, default=False)
    has_collections = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    grader_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    draft_date = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    payments = db.relationship('TripPayment', lazy='dynamic', backref='trip')
    grader_payments = db.relationship('GraderPayment', lazy='dynamic', backref='grader_payments')
    app_user = db.relationship('AppUser')


    def to_json(self):
        return {
            'trip_id':self.id,
            'grader_id':self.grader_id,
            'driver_id':self.driver_id,
            'vehicle_id': self.vehicle_id,
            'route_id': self.route_id,
        }


    
        


class GraderPayment(db.Model):
    __tablename__ = 'grader_payments'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    grader_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    is_paid = db.Column(db.Boolean, default=False)
    payment_generated = db.Column(db.Boolean, default=False)
    total_weight_collected = db.Column(db.Float, default=0.0)
    total_weight_received = db.Column(db.Float, default=0.0)
    grader_payment = db.Column(db.Float, default=0.0)
    grader_payment_status = db.Column(db.Boolean, default=0)
    collection_date = db.Column(db.DateTime())
    draft_date = db.Column(db.DateTime(), default=datetime.now)

class TripPayment(db.Model):
    __tablename__ = 'trip_payments'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    rate = db.Column(db.Float, default=0.0)
    weight = db.Column(db.Float, default=0.0)
    kdb = db.Column(db.Float, default=0.0)
    gross = db.Column(db.Float, default=0.0)
    net = db.Column(db.Float, default=0.0)
    farmer_loan_amount= db.Column(db.Float, default=0.0)
    is_paid = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'))
    farmer_advance_id = db.Column(db.Integer, db.ForeignKey('farmer_advance.id'))
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    delivery_date = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)


    def to_json(self):
        return {
            
            'farmer_id':self.farmer_id,
            'farmer_loan_amount':self.farmer_loan_amount,
            'Unpaid_amount':self.net
        }

class FarmerPayment(db.Model):
    __tablename__ = 'farmer_payment'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))



class Disbursed(db.Model):
    __tablename__ = 'farmer_payments'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    amount = db.Column(db.Float, default=0.0)
    


class FarmerContract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    produce_id = db.Column(db.Integer, db.ForeignKey('produce.id'))
    contract_no = db.Column(db.String(20), unique=True, index=True)
    payment_term = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    factory_id = db.Column(db.Integer, db.ForeignKey('factories.id'))
    valid_from = db.Column(db.DateTime(), default=datetime.now)
    valid_to = db.Column(db.DateTime(), )
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)
    payments = db.relationship('TripPayment', lazy='dynamic', backref='payment')
    # collections = db.relationship('Collection', lazy='dynamic', backref='collection')

    def __repr__(self):
        return self.farmer


class FarmerAdvance(db.Model):
    __tablename__ = 'farmer_advance'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    valid_from = db.Column(db.DateTime(), default=datetime.now)
    valid_to = db.Column(db.DateTime(), )
    draft_date = db.Column(db.DateTime(), default=datetime.now)
    amount = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)
    payments_farmer = db.relationship('TripPayment', lazy='dynamic', backref='payment_farmer')
    total_advance = db.Column(db.Float, default=0.0)
   

    def __repr__(self):
        return self.farmer





class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    draft_date = db.Column(db.DateTime(), default=datetime.now)

    def to_json(self):
        return {
            'code':self.code,
            'name':self.name,
        }


    def __repr__(self):
        return self.name

# class CollectionGrader(db.Model):
#     __tablename__ = 'collection_grader'
#     id = db.Column(db.Integer, primary_key=True)
#     trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
#     grader_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
#     payment_generated = db.Column(db.Boolean, default=False)
#     produce_weight = db.Column(db.Float)
#     total_weight_collected = db.Column(db.Float, default=0.0)
#     total_weight_received = db.Column(db.Float, default=0.0)
#     grader_payment = db.Column(db.Float, default=0.0)
#     grader_payment_status = db.Column(db.String(20), index=True)
#     collection_date = db.Column(db.DateTime())
#     draft_date = db.Column(db.DateTime(), default=datetime.now)

class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    device_imei = db.Column(db.String(50))
    transfer_code = db.Column(db.String(50))
    receipt_no = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    centre_id = db.Column(db.Integer, db.ForeignKey('collection_centres.id'))
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    produce_id = db.Column(db.Integer, db.ForeignKey('produce.id'))
    # contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    payment_generated = db.Column(db.Boolean, default=False)
    invalidated = db.Column(db.Boolean)
    produce_weight = db.Column(db.Float)
    collection_date = db.Column(db.DateTime())
    draft_date = db.Column(db.DateTime(), default=datetime.now)


    def from_json(self, json):
        try:
            supplier_number = json['supplier_number']
            produce_code = json['produce_code']
            produce_weight = json['produce_weight']
            device_imei = json['device_imei']
            centre_code = json['centre_code']
            receipt_no = json['receipt_no']
            username = json['username']
            trip_id = json['trip_id']
            collection_date = json['collection_date']
            collection_date = datetime.strptime(collection_date, "%Y-%m-%d %H:%M")
            record_id = json['record_id']
            if record_id == 0:
                transfer_code = json['transfer_code']
                farmer = Farmer.query.filter_by(supplier_no=supplier_number).first()
                produce = Produce.query.filter_by(code=produce_code).first()
                centre = CollectionCentre.query.filter_by(code=centre_code).first()
                user = AppUser.query.filter_by(username=username).first()
                self.device_imei = device_imei
                self.receipt_no = receipt_no
                self.user_id = user.id
                self.centre_id = centre.id
                self.farmer_id = farmer.id
                self.produce_id = produce.id
                self.produce_weight = produce_weight
                self.collection_date = collection_date
                self.trip_id = trip_id
                return self
            else:
                return "ERROR: DUPLICATE RECORD"
        except KeyError as e:
            error = "ERROR: Invalid collections data: missing "+e.args[0]
            print(error)
            return error

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    name = db.Column(db.String)


    def to_json(self):
        return {
            'name':self.name,
            'code':self.code
        }
    
    def __repr__(self):
        return self.name

class Licence(db.Model):
    __tablename__ = 'licence'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.DateTime, )
    end_date = db.Column(db.DateTime, )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    interest = db.Column(db.Float, default=0.0)
    loan_status = db.Column(db.Boolean, default=True)
    loan_amount = db.Column(db.Float, default=True)
    repaid_amount = db.Column(db.Float, default=True)
    repayment_date = db.Column(db.DateTime, )
    date_disturbsment = db.Column(db.DateTime, )
    balane= db.Column(db.Float, default=True)
    total_loan_amount = db.Column(db.Float, default=0.0)


        
        
