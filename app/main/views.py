from datetime import datetime, date
from sqlalchemy import Date, cast
from sqlalchemy.sql.functions import func
from flask import render_template, session, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user, LoginManager
from .forms import FarmersUploadForm, FactoryForm, LicenceForm, LimitForm, CooperativeForm, SocietyForm, CentreForm, GroupForm, ProcessorForm, CollectionPerGrader, ProduceForm, FarmersForm, SeasonForm, ContractForm, RouteForm,VehicleForm, GraderForm, DriverForm, TripForm, CompleteTripForm, AdvanceForm
from ..models import Factory, CollectionCentre, Licence, Society, Produce, Group, FarmerAdvance, Processor, Farmer, Season, Collection, Cooperative, FarmerContract, Route, Vehicle, AppUser, Role, Driver, Trip, TripPayment, GraderPayment, FarmerPayment, Disbursed
from app import db
from werkzeug.utils import secure_filename
import os
import uuid
import re
import csv
from pprint import pprint

from . import main

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # LECH CODE HERE
    farmer_count = Farmer.query.count()
    graders_count = AppUser.query.count()
    routes_count = Route.query.count()
    centre_count = CollectionCentre.query.count()
    return render_template('main/dashboard.html', centre_count=centre_count, farmers_count=farmer_count, graders_count=graders_count, routes_count=routes_count)

@main.route('/cooperative', methods=['GET', 'POST'])
@login_required
def cooperative():
    cooperative = Cooperative.query.all()
    return render_template('main/cooperative.html', cooperative=cooperative)


@main.route('/new-cooperative', methods=['GET', 'POST'])
@login_required
def new_cooperative():
    form = CooperativeForm()
    if form.validate_on_submit():
        cooperative = Cooperative(code=form.code.data, name=form.name.data, creator=current_user)
        db.session.add(cooperative)
        db.session.commit()
        flash('The Cooperative Union  was added successfully.', 'success')
        return redirect(url_for('.cooperative'))
    return render_template('main/new_cooperative.html', form=form)


@main.route('/society', methods=['GET', 'POST'])
@login_required
def society():
    society = Society.query.all()
    return render_template('main/society.html', society=society)


@main.route('/new-society', methods=['GET', 'POST'])
@login_required
def new_society():
    form = SocietyForm()
    form.cooperative.choices = [(row.id, row.name) for row in Cooperative.query.all()]
    if form.validate_on_submit():
        society = Society(code=form.code.data, name=form.name.data, creator=current_user,  cooperative_id=form.cooperative.data)
        db.session.add(society)
        db.session.commit()
        flash('The Society  was added successfully.', 'success')
        return redirect(url_for('.society'))
    return render_template('main/new_society.html', form=form)

@main.route('/factories', methods=['GET', 'POST'])
@login_required
def factories():
    factories = Factory.query.all()
    return render_template('main/factories.html', factories=factories)


@main.route('/new-factory', methods=['GET', 'POST'])
@login_required
def new_factory():
    form = FactoryForm()
    if form.validate_on_submit():
        factory = Factory(name=form.name.data, creator=current_user)
        db.session.add(factory)
        db.session.commit()
        flash('The factory was added successfully.', 'success')
        return redirect(url_for('.factories'))
    return render_template('main/new_factory.html', form=form)


@main.route('/factory/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_factory(id):
    factory = Factory.query.get_or_404(id)
    form = FactoryForm()
    form.name.data = factory.name
    if form.validate_on_submit():
        factory.name = request.form.get('name')
        db.session.add(factory)
        db.session.commit()
        flash('The factory was updated successfully.', 'success')
        return redirect(url_for('.factories'))
    return render_template('main/new_factory.html', form=form)

@main.route('/seasons', methods=['GET', 'POST'])
@login_required
def seasons():
    seasons = Season.query.all()
    return render_template('main/seasons.html', seasons=seasons)


@main.route('/new-season', methods=['GET', 'POST'])
@login_required
def new_season():
    form = SeasonForm()
    if form.validate_on_submit():
        season = Season(code=form.code.data, name=form.name.data, creator=current_user)
        db.session.add(season)
        db.session.commit()
        flash('The season was added successfully.', 'success')
        return redirect(url_for('.seasons'))
    return render_template('main/new_season.html', form=form)
    


@main.route('/produce', methods=['GET', 'POST'])
@login_required
def produce():
    produce = Produce.query.all()
    return render_template('main/produce.html', produce=produce)


@main.route('/new-produce', methods=['GET', 'POST'])
@login_required
def new_produce():
    form = ProduceForm()
    if form.validate_on_submit():
        produce = Produce(code=form.code.data, name=form.name.data, creator=current_user)
        db.session.add(produce)
        db.session.commit()
        flash('The Produce was added successfully.', 'success')
        return redirect(url_for('.produce'))
    return render_template('main/new_produce.html', form=form)


@main.route('/produce/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_produce(id):
    produce = Produce.query.get_or_404(id)
    form = ProduceForm()
    form.code.data = produce.code
    form.name.data = produce.name
    form.cess.data = produce.cess
    if form.validate_on_submit():
        produce.code = request.form.get('code')
        produce.name = request.form.get('name')
        produce.cess = request.form.get('cess')
        db.session.add(produce)
        db.session.commit()
        flash('The produce was updated successfully.', 'success')
        return redirect(url_for('.produce'))
    return render_template('main/new_produce.html', form=form)


@main.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    groups = Group.query.all()
    return render_template('main/groups.html', groups=groups)

@main.route('/new-group', methods=['GET', 'POST'])
@login_required
def new_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(code=form.code.data, name=form.name.data, creator=current_user)
        db.session.add(group)
        db.session.commit()
        flash('The Group was added successfully.', 'success')
        return redirect(url_for('.groups'))
    return render_template('main/new_group.html', form=form)


@main.route('/group/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    group = Group.query.get_or_404(id)
    form = GroupForm()
    form.code.data = group.code
    form.name.data = group.name
    if form.validate_on_submit():
        group.code = request.form.get('code')
        group.name = request.form.get('name')
        db.session.add(group)
        db.session.commit()
        flash('The group was updated successfully.', 'success')
        return redirect(url_for('.groups'))
    return render_template('main/new_group.html', form=form)


@main.route('/processors', methods=['GET', 'POST'])
@login_required
def processors():
    processors = Processor.query.all()
    return render_template('main/processors.html', processors=processors)


@main.route('/new-processor', methods=['GET', 'POST'])
@login_required
def new_processor():
    form = ProcessorForm()
    if form.validate_on_submit():
        processor = Processor(code=form.code.data, name=form.name.data, creator=current_user)
        db.session.add(processor)
        db.session.commit()
        flash('The Processor was added successfully.', 'success')
        return redirect(url_for('.processors'))
    return render_template('main/new_processor.html', form=form)


@main.route('/processor/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_processor(id):
    processor = Processor.query.get_or_404(id)
    form = ProcessorForm()
    form.code.data = processor.code
    form.name.data = processor.name
    if form.validate_on_submit():
        processor.code = request.form.get('code')
        processor.name = request.form.get('name')
        db.session.add(processor)
        db.session.commit()
        flash('The processor was updated successfully.', 'success')
        return redirect(url_for('.processors'))
    return render_template('main/new_processor.html', form=form)


@main.route('/centres', methods=['GET', 'POST'])
@login_required
def centres():
    centres = CollectionCentre.query.all()
    return render_template('main/centres.html', centres=centres)


@main.route('/routes', methods=['GET', 'POST'])
@login_required
def routes():
    routes = Route.query.all()
    return render_template('main/routes.html', routes=routes)


@main.route('/new-route', methods=['GET', 'POST'])
@login_required
def new_route():
    form = RouteForm()
    if form.validate_on_submit():
        route = Route(name=form.name.data, start=form.start.data, end=form.end.data, creator=current_user)
        db.session.add(route)
        db.session.commit()
        flash('Route was added successfully.', 'success')
        return redirect(url_for('.routes'))
    return render_template('main/new_route.html', form=form)


@main.route('/route/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_route(id):
    route = Route.query.get_or_404(id)
    form = RouteForm()
    form.name.data = route.name
    if form.validate_on_submit():
        route.name = request.form.get('name')
        db.session.add(route)
        db.session.commit()
        flash('The route was updated successfully.', 'success')
        return redirect(url_for('.routes'))
    return render_template('main/new_route.html', form=form)



@main.route('/new-vehicle', methods=['GET', 'POST'])
@login_required
def new_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        vehicle = Vehicle(reg_no=form.reg_no.data, make=form.make.data, ownership=form.ownership.data, color=form.color.data, body=form.body.data, creator=current_user)
        db.session.add(vehicle)
        db.session.commit()
        flash('Motor Vehicle added successfully.', 'success')
        return redirect(url_for('.vehicles'))
    return render_template('main/new_vehicle.html', form=form)


@main.route('/vehicle/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    form = VehicleForm()
    form.reg_no.data = vehicle.reg_no
    form.make.data = vehicle.make
    form.ownership.data = vehicle.ownership
    form.color.data = vehicle.color
    form.body.data = vehicle.body
    if form.validate_on_submit():
        vehicle.reg_no = request.form.get('reg_no')
        vehicle.make = request.form.get('make')
        vehicle.ownership = request.form.get('ownership')
        vehicle.color = request.form.get('color')
        vehicle.body = request.form.get('body')
        db.session.add(vehicle)
        db.session.commit()
        flash('The vehicle was updated successfully.', 'success')
        return redirect(url_for('.vehicles'))
    return render_template('main/new_vehicle.html', form=form)


@main.route('/vehicles', methods=['GET', 'POST'])
@login_required
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template('main/vehicles.html', vehicles=vehicles)


@main.route('/graders', methods=['GET', 'POST'])
@login_required
def graders():
    objects = AppUser.query.all()
    return render_template('main/graders.html', objects=objects)




@main.route('/new_grader', methods=['GET', 'POST'])
@login_required
def new_grader():
    form = GraderForm()
    form.role.choices = [(row.id, row.name) for row in Role.query.all()]
    if form.validate_on_submit():
        grader = AppUser(
                first_name=form.first_name.data, 
                last_name=form.last_name.data, 
                phone_number=form.phone_number.data, 
                contract_price=form.contract_price.data, 
                username=form.app_username.data, 
                app_password=form.app_password.data, 
                creator=current_user,
                role_id = form.role.data
            )
        db.session.add(grader)
        db.session.commit()
        flash('Grader added successfully.', 'success')
        return redirect(url_for('.graders'))
    return render_template('main/new_grader.html', form=form)



@main.route('/grader/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_grader(id):
    grader = AppUser.query.get_or_404(id)
    form = GraderForm(role=grader.role_id)
    form.first_name.data = grader.first_name
    form.last_name.data = grader.last_name
    form.phone_number.data = grader.phone_number
    form.contract_price.data = grader.contract_price
    form.app_username.data = grader.username
    form.app_password.data = grader.app_password
    form.role.choices = [(row.id, row.name) for row in Role.query.all()]
    if form.validate_on_submit():
        grader.first_name = request.form.get('first_name')
        grader.last_name = request.form.get('last_name')
        grader.phone_number = request.form.get('phone_number')
        grader.contract_price = request.form.get('contract_price')
        grader.username = request.form.get('app_username')
        grader.app_password = request.form.get('app_password')
        grader.role_id = request.form.get('role')
        db.session.add(grader)
        db.session.commit()
        flash('The grader was updated successfully.', 'success')
        return redirect(url_for('.graders'))
    return render_template('main/new_grader.html', form=form)


@main.route('/grader/<int:id>/trips', methods=['GET', 'POST'])
@login_required
def grader_trips(id):
    grader = AppUser.query.get_or_404(id)
    objects = Trip.query.filter_by(grader_id=grader.id)
    return render_template('main/grader_trips.html', objects=objects, grader=grader)

@main.route('/driver/<int:id>/trips', methods=['GET', 'POST'])
@login_required
def driver_trips(id):
    driver = Driver.query.get_or_404(id)
    objects = Trip.query.filter_by(driver_id=driver.id) # SELECT * FROM TRIPS WHERE driver_id = 121
    return render_template('main/driver_trips.html', objects=objects, driver=driver)






@main.route('/drivers')
@login_required
def drivers():
    drivers = Driver.query.all()
    return render_template('main/drivers.html', objects=drivers)



def get_farmer_info(phone_number):
    farmer_data = Farmer.query.filter_by(phone_number = phone_number)
    return farmer_data.id

def get_farmer_id(id):
    farmer_data = Farmer.query.filter_by(farmer_id = id)
    return farmer_data;


@main.route('/new_driver', methods=['GET', 'POST'])
@login_required
def new_driver():
    form = DriverForm()
    if form.validate_on_submit():
        driver = Driver(
                first_name=form.first_name.data, 
                last_name=form.last_name.data, 
                phone_number=form.phone_number.data,
                creator=current_user
            )
        db.session.add(driver)
        db.session.commit()
        flash('Driver added successfully.', 'success')
        return redirect(url_for('.drivers'))
    return render_template('main/new_driver.html', form=form)


@main.route('/driver/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_driver(id):
    driver = Driver.query.get_or_404(id)
    form = DriverForm()
    form.first_name.data = driver.first_name
    form.last_name.data = driver.last_name
    form.phone_number.data = driver.phone_number
    if form.validate_on_submit():
        driver.first_name = request.form.get('first_name')
        driver.last_name = request.form.get('last_name')
        driver.phone_number = request.form.get('phone_number')
        db.session.add(driver)
        db.session.commit()
        flash('The driver was updated successfully.', 'success')
        return redirect(url_for('.drivers'))
    return render_template('main/new_driver.html', form=form)




@main.route('/stations', methods=['GET', 'POST'])
@login_required
def stations():
    stations = CollectionCentre.query.all()
    return render_template('main/stations.html', stations=stations)



@main.route('/new-centre', methods=['GET', 'POST'])
@login_required
def new_centre():
    form = CentreForm()
    form.route.choices = [(row.id, row.name) for row in Route.query.all()]
    if form.validate_on_submit():
        centre = CollectionCentre(code=form.code.data, name=form.name.data, collection_centres_creator=current_user, route_id=form.route.data)
        db.session.add(centre)
        db.session.commit()
        flash('The centre was added successfully.', 'success')
        return redirect(url_for('.centres'))
    return render_template('main/new_centre.html', form=form)

@main.route('/centre/<int:id>/farmers', methods=['GET', 'POST'])
@login_required
def centre_farmers(id):
    centre = CollectionCentre.query.get_or_404(id)
    farmers = Farmer.query.filter_by(centre_id=centre.id)
    return render_template('main/centre_farmers.html', farmers=farmers, centre=centre)




@main.route('/centre/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_centre(id):
    centre = CollectionCentre.query.get_or_404(id)
    form = CentreForm(route=centre.route_id)
    form.code.data = centre.code
    form.name.data = centre.name
    form.route.choices = [(row.id, row.name) for row in Route.query.all()]
    if form.validate_on_submit():
        centre.code = request.form.get('code')
        centre.name = request.form.get('name')
        centre.route_id = request.form.get('route')
        db.session.add(centre)
        db.session.commit()
        flash('The centre was updated successfully.', 'success')
        return redirect(url_for('.centres'))
    return render_template('main/new_centre.html', form=form)



@main.route('/farmers')
@login_required
def farmers():
    farmers = Farmer.query.all()
    return render_template('main/farmers.html', farmers=farmers)

def get_farmer(id):
    return Farmer.query.filter_by(id=id).first()

def get_farmer_contract(farmer_id):
    return FarmerContract.query.filter(FarmerContract.farmer_id == farmer_id, FarmerContract.active == True).first()

def get_farmer_collection(farmer_id):
    return FarmerContract.query.filter(FarmerContract.farmer_id == farmer_id, FarmerContract.active == True).first()

def get_total_farmer_advance(farmer_id):
    total_advance = db.session.query(FarmerAdvance.farmer_id, func.sum(FarmerAdvance.amount ).label('total_advance')).filter(FarmerAdvance.farmer_id == farmer_id).all()
    return total_advance


def get_farmer_payment(farmer_id):
    farmer_cumm = get_gross_payment(contract.price, col.produce_weight) 

    return farmer_cumm


@main.route('/cumm-farmers', methods=['GET', 'POST'])
@login_required
def cumm_farmer():
    # data = Farmer.query.all()

    start_date =date.today().replace(day=1)
    #end_date = datetime.strptime(form.end_date.data, "%m/%d/%Y %H:%M %p").date() #

    data = db.session.query(TripPayment.farmer_id, func.sum(TripPayment.net ).label('net'), func.sum(TripPayment.net * 0.75).label('farmer_loan_amount')).filter(TripPayment.status == 'NOT PAID' ).group_by(TripPayment.farmer_id).all()
    


    return render_template('main/farmer_cumm.html', data=data, start_date= start_date)



@main.route('/loan-limit', methods=['GET', 'POST'])
@login_required
def loan_limit():
   
    


    return render_template('main/farmer_cumm.html')



@main.route('/advance', methods=['GET', 'POST'])
@login_required
def advance():
    # advance = Advance.query.all()
    return render_template('main/advance.html')



@main.route('/licence', methods=['GET', 'POST'])
@login_required
def licence():
    if current_user.role_id == 3:
        licences = Licence.query.all()
        return render_template('main/licence.html', licences = licences)
    else:
        return redirect('/')

@main.route('/new-licence', methods=['GET', 'POST'])
@login_required
def new_licence():
    form = LicenceForm()
    if form.validate_on_submit():
        licence = Licence(start_date=form.start_date.data, end_date=form.end_date.data, creator=current_user)
        db.session.add(licence)
        db.session.commit()
        flash('The Licence was added successfully.', 'success')
        return redirect(url_for('.licence'))
    return render_template('main/new_licence.html', form=form)

@main.route('/farmer/<int:id>')
@login_required
def farmer(id):
    farmer = Farmer.query.get_or_404(id)
    contract_farmer = db.session.query(FarmerContract.price)
    contracts = FarmerContract.query.filter_by(farmer_id=farmer.id)
    advances = FarmerAdvance.query.filter_by(farmer_id=farmer.id)
    collections = Collection.query.filter_by(farmer_id=farmer.id)
    total_advance = db.session.query(FarmerAdvance.farmer_id, func.sum(FarmerAdvance.amount * 100).label('total_advance')).group_by(FarmerAdvance.farmer_id).all()
    farmer_cumm =  db.session.query(Collection.farmer_id, func.sum(Collection.produce_weight)
        ).group_by(Collection.farmer_id).all()



    return render_template('main/farmer.html', farmer=farmer, collections=collections, contracts=contracts,  advances=advances, total_advance=total_advance, farmer_cumm=farmer_cumm)



@main.route('/farmer/<int:id>/new-contract', methods=['GET', 'POST'])
@login_required
def new_contract(id):
    farmer = Farmer.query.get_or_404(id)
    form = ContractForm()
    form.factory.choices = [(row.id, row.name) for row in Factory.query.all()]
    form.produce.choices = [(row.id, row.name) for row in Produce.query.all()]
    if form.validate_on_submit():
        # Deactivate current contract
        contract_no = farmer.supplier_no
        cuurent_contract = FarmerContract.query.filter(FarmerContract.farmer_id == farmer.id, FarmerContract.active == True).first()
        if cuurent_contract:
            contract_no = farmer.supplier_no + "-" + str(cuurent_contract.id)
            cuurent_contract.active = False
            db.session.add(cuurent_contract)
        contract = FarmerContract(
            produce_id=form.produce.data, 
            farmer_id=farmer.id, 
            contract_no=contract_no, 
            factory_id=form.factory.data, 
            price=form.price.data,
            payment_term=form.payment_term.data
        )
        db.session.add(contract)
        db.session.commit()
        flash('Contract added successfully.', 'success')
        return redirect(url_for('.farmer', id=farmer.id))
    return render_template('main/new_contract.html', farmer=farmer, form=form)



@main.route('/farmer/<int:id>/new-farmer-advance', methods=['GET', 'POST'])
@login_required
def new_farmer_advance(id):
    farmer = Farmer.query.get_or_404(id)
    form = AdvanceForm()
    if form.validate_on_submit():
        # Deactivate current contract
        
        current_advance = FarmerAdvance.query.filter(FarmerAdvance.farmer_id == farmer.id, FarmerAdvance.active == True).first()
        if current_advance:
            current_advance.active = False
            db.session.add(current_advance)
        advance = FarmerAdvance( 
            farmer_id=farmer.id, 
            amount=form.amount.data,
        )
        db.session.add(advance)
        db.session.commit()
        flash('Advance added successfully.', 'success')
        return redirect(url_for('.farmer', id=farmer.id))
    return render_template('main/new_advance.html', farmer=farmer, form=form)


@main.route('/trips', methods=['GET', 'POST'])
@login_required
def trips():
    objects = Trip.query.all()
    return render_template('main/trips.html', objects=objects )

@main.route('/new_trip', methods=['GET', 'POST'])
@login_required
def new_trip():
    form = TripForm()
    form.route.choices = [(row.id, row.name) for row in Route.query.all()]
    form.grader.choices = [(row.id, row.fullname) for row in AppUser.query.filter_by(role_id=2)]
    form.driver.choices = [(row.id, row.fullname) for row in Driver.query.all()]
    form.vehicle.choices = [(row.id, row.reg_no) for row in Vehicle.query.all()]
    if form.validate_on_submit():


        status = db.Column(db.String(20), unique=True, index=True)
        total_weight_collected = db.Column(db.Float)
        total_weight_received = db.Column(db.Float)
        trip_date = datetime.strptime(form.trip_date.data,"%m/%d/%Y %I:%M %p")
        trip = Trip(
                draft_date = trip_date,
                route_id=form.route.data, 
                driver_id=form.driver.data, 
                vehicle_id=form.vehicle.data, 
                grader_id=form.grader.data, 
                user_id=current_user.id,
                status="OPEN"
            )
        db.session.add(trip)
        db.session.commit()
        flash('Trip scheduled successfully.', 'success')
        return redirect(url_for('.trips'))
    return render_template('main/new_trip.html', form=form)




@main.route('/trip/<int:id>/collections', methods=['GET', 'POST'])
@login_required
def trip_collections(id):
    trip = Trip.query.get_or_404(id)
    variance = (trip.total_weight_received) - (trip.total_weight_collected)
    grader_payment = (trip.total_weight_received) * 1
    collections = Collection.query.filter(Collection.trip_id == trip.id).all()
    payments = TripPayment.query.filter_by(trip_id=trip.id)
    return render_template('main/trip_collections.html', variance=variance,  grader_payment= grader_payment, collections=collections, trip=trip, payments=payments)




@main.route('/trip/<int:trip_id>/collection/<int:collection_id>', methods=['GET', 'POST'])
@login_required
def invalidate_collection(trip_id, collection_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.status == "CLOSED":
        flash("TRIP ALREADY CLOSED. YOU CAN NOT INVALIDATE COLLECTIONS FOR A CLOSED TRIP", "error")
        return redirect(url_for('.edit_trip', id=trip.id))
    collection = Collection.query.get_or_404(collection_id)
    collection.invalidated = True
    db.session.add(trip)
    db.session.commit()
    flash('Collection Invalidated Successfully.', 'success')
    return redirect(url_for('.edit_trip', id=trip.id))

@main.route('/trip/<int:trip_id>/collection/validate/<int:collection_id>', methods=['GET', 'POST'])
@login_required
def validate_collection(trip_id, collection_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.status == "CLOSED":
        flash("TRIP ALREADY CLOSED. YOU CAN NOT VALIDATE COLLECTIONS FOR A CLOSED TRIP", "error")
        return redirect(url_for('.edit_trip', id=trip.id))
    collection = Collection.query.get_or_404(collection_id)
    collection.invalidated = False
    db.session.add(trip)
    db.session.commit()
    flash('Collection Validated Successfully.', 'success')
    return redirect(url_for('.edit_trip', id=trip.id))


@main.route('/trip/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_trip(id):
    variance = 0
    trip = Trip.query.get_or_404(id)
    variance = (trip.total_weight_received) - (trip.total_weight_collected)
    grader_payment = (trip.total_weight_received) * 1

    collections = Collection.query.filter(Collection.trip_id == trip.id).all()
    invalidated_collections = Collection.query.filter(Collection.invalidated == True, Collection.trip_id == trip.id).all()

    payments = TripPayment.query.filter_by(trip_id=trip.id)
    form = CompleteTripForm()
    if request.method == 'POST':
        if trip.status == "CLOSED":
            flash("TRIP ALREADY CLOSED", "error")
            return redirect(url_for('.edit_trip', id=trip.id))
        if form.validate_on_submit():
            trip.total_weight_received = form.total_weight_received.data
            trip.status = "CLOSED"
            db.session.add(trip)
            db.session.commit()
            flash('Trip Completed successfully.', 'success')
            return redirect(url_for('.edit_trip', id=trip.id))
    return render_template('main/edit_trip.html', variance=variance, collections=collections, grader_payment= grader_payment, invalidated_collections=invalidated_collections, form=form, trip=trip, payments=payments)




def get_gross_payment(rate, weight):
    return rate * weight

def get_farmer_total_advance(amount):
    return FarmerAdvance.query.count(amount)

def get_net_payment(gross, kdb):
    return gross-kdb - 5

def get_kdb_amount(weight):
    produce = Produce.query.first()
    rate = produce.cess
    return weight*rate




@main.route('/trip/<int:id>/payments', methods=['GET', 'POST'])
@login_required
def generate_trip_payments(id):
    trip = Trip.query.get_or_404(id)
    if trip.status == "OPEN":
        flash("TRIP STILL OPEN. CLOSE THE TRIP FIRST BEFORE GENERATING PAYMENTS", "error")
        return redirect(url_for('.edit_trip', id=trip.id))
    collections = Collection.query.filter(Collection.invalidated.isnot(True), Collection.payment_generated.isnot(True), Collection.trip_id == trip.id)
    
    for col in collections:
        contract = get_farmer_contract(col.farmer_id)
        farmer = Farmer.query.filter_by(id=col.farmer_id).first()
        if not contract:
            flash("FARMER {} HAS NO CONTRACT. SETUP HIS CONTRACT FIRST BEFORE GENERATING PAYMENTS".format(farmer.fullname), "error")
            return redirect(url_for('.edit_trip', id=trip.id))
        payment = TripPayment(
            status = "NOT PAID",
            rate = contract.price,
            kdb = get_kdb_amount(col.produce_weight),
            weight = col.produce_weight,
            gross = get_gross_payment(contract.price, col.produce_weight),
            net = get_net_payment(get_gross_payment(contract.price, col.produce_weight), get_kdb_amount(col.produce_weight)),
            trip_id = trip.id,
            contract_id = contract.id,
            farmer_id = col.farmer_id,
            delivery_date = col.collection_date
            )
        col.payment_generated = True
        db.session.add(col)
        db.session.add(payment)
    db.session.commit()
    flash('Payments Generated successfully.', 'success')
    return redirect(url_for('.edit_trip', id=trip.id))


@main.route('/grader_payment', methods=['GET', 'POST'])
@login_required
def grader_payment():

    grader_collections = Trip.query.all()
    return render_template('main/grader_payment.html', grader_collections = grader_collections)

@main.route('/grader_payment', methods=['GET', 'POST'])
@login_required
def generate_grader_payment():

    grader_collection = Trip.query.filter(Trip.payment_grader_status.isnot(True)).all()

    for col in grader_collection:
        payment = Trip(
            payment_grader_status = "UNPAID",
            grader_id = grader.id,
            total_weight_received =col.total_weight_received,
            grader_payment =col.grader_payment
            
            )
        col.payment_generated = True
        db.session.add(col)
        db.session.add(payment)
        db.session.commit()
    
    return render_template('main/grader_payment.html', payment= grader_payments)


# def get_total_collection():
#     total_collections = db.session.query(db.func.sum(Collection.produce_weight))
#     return get_total_collection()

@main.route('/collections')
@login_required
def collections():
    total_collection = db.session.query(db.func.sum(Collection.produce_weight))
    # #Collection.query(db.func.count(Collection.produce_weight))
    collections = Collection.query.all()
    return render_template('main/collections.html', collections=collections, total_collection=total_collection)






@main.route('/new-farmer', methods=['GET', 'POST'])
@login_required
def new_farmer():
    form = FarmersForm()
    upload_form = FarmersUploadForm()
    form.centre.choices = [(row.id, row.name) for row in CollectionCentre.query.all()]
    # form.group.choices = [(row.id, row.name) for row in Group.query.all()]
    if form.validate_on_submit():
        farmer = Farmer(
            supplier_no=form.supplier_no.data, 
            first_name=form.first_name.data, 
            last_name=form.last_name.data, 
            creator=current_user, 
            centre_id=form.centre.data,
            # group_id=form.group.data,
            id_number = form.id_number.data,
            phone_number = form.phone_number.data
        )
        db.session.add(farmer)
        db.session.commit()
        flash('The farmer was added successfully. Create a new contract for the farmer now', 'success')
        return redirect(url_for('.farmers'))
    return render_template('main/new_farmer.html', form=form, upload_form=upload_form)



@main.route('/farmer/edit/<int:id>/deactivte', methods=['GET', 'POST'])
@login_required
def deactivate_farmer(id):
    farmer = Farmer.query.get_or_404(id)
    farmer.status = "INACTIVE"
    db.session.add(farmer)
    db.session.commit()
    return redirect(url_for('.farmer', id=farmer.id))

@main.route('/farmer/edit/<int:id>/activate', methods=['GET', 'POST'])
@login_required
def activate_farmer(id):
    farmer = Farmer.query.get_or_404(id)
    farmer.status = "ACTIVE"
    db.session.add(farmer)
    db.session.commit()
    return redirect(url_for('.farmer', id=farmer.id))

@main.route('/farmer/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_farmer(id):
    farmer = Farmer.query.get_or_404(id)
    upload_form = FarmersUploadForm()
    form = FarmersForm(centre=farmer.centre_id, obj=farmer)#need to add group like centre here
    form.centre.choices = [(row.id, row.name) for row in CollectionCentre.query.all()]
    if form.validate_on_submit():
        farmer.route_id = request.form.get('route')
        farmer.supplier_no=request.form.get('supplier_no')
        farmer.first_name=request.form.get('first_name')
        farmer.last_name=form.last_name.data
        farmer.centre_id=request.form.get('centre')
        farmer.id_number = request.form.get('id_number')
        farmer.phone_number = request.form.get('phone_number')
        db.session.add(farmer)
        db.session.commit()
        flash('The farmer was updated successfully.', 'success')
        return redirect(url_for('.farmer', id=farmer.id))
    return render_template('main/new_farmer.html', form=form, upload_form=upload_form)

@main.route('/farmer-upload', methods=['GET', 'POST'])
def farmer_upload():
    form = FarmersUploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.farmers_csv.data.filename)
        extension = filename.rsplit('.', 1)[1]
        farmers_csv = str(uuid.uuid4()) + '.' + extension
        form.farmers_csv.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], farmers_csv))
        flash('The farmers were Staged successfully. After previewing the uploaded data you can go ahead and save it to database', 'success')
        return redirect(url_for('main.preview_import', file=farmers_csv.rsplit('.', 1)[0]))
    flash('Upload was not successful. Please check', 'error')
    return redirect(url_for('main.new_farmer'))


def read_csv_upload(file):
    data = []
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in spamreader:
            member = {}
            member['supplier_no'] = row[0].strip()
            member['first_name'] = row[1].strip()
            member['last_name'] = row[2].strip()
            member['id_number'] = row[3].strip()
            member['phone_number'] = row[4].strip()
            member['centre'] = row[5].strip()
            data.append(member)
    return data

@main.route('/preview-import/<file>')
def preview_import(file):
    data = read_csv_upload(os.path.join(current_app.config['UPLOAD_FOLDER'],file+".csv"))  
    return render_template('main/preview_import.html', data=data, csv_file=file)

def get_farmer_centre(centre):
    centreId = CollectionCentre.query.filter(CollectionCentre.name==centre).with_entities(CollectionCentre.id).first()
    return centreId

def get_farmer_group(group):
    return Group.query.filter(Group.name == group).first()

@main.route('/save-upload/<file>')
def save_upload(file):
    farmers = read_csv_upload(os.path.join(current_app.config['UPLOAD_FOLDER'],file+".csv"))
    for farmer in farmers:
        centreId = get_farmer_centre(farmer['centre'])
        
        farmer_obj = Farmer(
            supplier_no=farmer['supplier_no'], 
            first_name=farmer['first_name'], 
            last_name=farmer['last_name'], 
            creator=current_user, 
            id_number = farmer['id_number'],
            phone_number = farmer['phone_number'],
            centre_id = centreId
        )
        db.session.add(farmer_obj)
    db.session.commit()
    flash('The farmers upload have saved successfully. Create a new contracts for the farmers now', 'success')
    return redirect(url_for('.farmers'))





def get_amount_pkg_farmer(farmer_id):
  
    farmer_pkg = FarmerContract.query.filter(FarmerContract.farmer_id == farmer_id, FarmerContract.active == True).first()
    return farmer_pkg.price;