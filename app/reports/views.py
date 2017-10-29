from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import FactoryForm, CollectionPerGrader
from ..models import Factory, CollectionCentre, Produce, Farmer, Season, Collection, FarmerContract, Route, Vehicle, AppUser, Role, Driver, Trip
from app import db
from datetime import datetime
from sqlalchemy import func


from . import reports

@reports.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	form = FactoryForm()
	collection_per_grader_form = CollectionPerGrader()
	collection_per_grader_form.grader.choices = [(row.id, row.fullname) for row in AppUser.query.filter_by(role_id=2)]
	return render_template('reports/reports.html', form=form, collection_per_grader_form=collection_per_grader_form)



@reports.route('/collection-per-grader', methods=['GET', 'POST'])
@login_required
def collection_per_grader():
	form = CollectionPerGrader()
	form.grader.choices = [(row.id, row.fullname) for row in AppUser.query.filter_by(role_id=2)]

	
	start_date = datetime.strptime(form.start_date.data, "%m/%d/%Y %H:%M %p").date() #
	end_date = datetime.strptime(form.end_date.data, "%m/%d/%Y %H:%M %p").date() #

	trips = Trip.query.filter_by(grader_id = form.grader.data)

	trips_ids = [item.id for item in Trip.query.filter_by(grader_id = form.grader.data).all()]
	report_data = Collection.query.filter(Collection.trip_id.in_(trips_ids), Collection.collection_date >= start_date, Collection.collection_date <= end_date)
	return render_template('reports/collection_per_grader.html', form=form, data=report_data, start_date=start_date, end_date=end_date)

def get_grader_fullname(id):
	return AppUser.query.filter_by(id=id).first()

def get_farmer(id):
	return Farmer.query.filter_by(id=id).first()

@reports.route('/grader-variance', methods=['GET', 'POST'])
@login_required
def grader_variance():
	form = CollectionPerGrader()

	start_date = datetime.strptime(form.start_date.data, "%m/%d/%Y %H:%M %p").date() 
	end_date = datetime.strptime(form.end_date.data, "%m/%d/%Y %H:%M %p").date() 

	trips = db.session.query(Trip.grader_id, func.sum(Trip.total_weight_collected), func.sum(Trip.total_weight_received)
		).filter(Trip.draft_date  >= start_date, Trip.draft_date <= end_date
		).group_by(Trip.grader_id).all()
	data = []
	for trip in trips:
		grader_data = {}
		grader_data['grader_id'] = trip[0]
		grader_data['grader_name'] = get_grader_fullname(trip[0])
		grader_data['total_weight_collected'] = trip[1]
		grader_data['total_weight_received'] = trip[2]
		grader_data['variance'] = trip[2] - trip[1]

		data.append(grader_data)

	return render_template('reports/grader_variance.html', data=data, start_date=start_date, end_date=end_date)

@reports.route('/cumm-farmers', methods=['GET', 'POST'])
@login_required
def cumm_farmer():
	form = CollectionPerGrader()

	start_date = datetime.strptime(form.start_date.data, "%m/%d/%Y %H:%M %p").date() 
	end_date = datetime.strptime(form.end_date.data, "%m/%d/%Y %H:%M %p").date() 

	trips = db.session.query(Collection.farmer_id, func.sum(Collection.produce_weight)
		).filter(Collection.collection_date  >= start_date, Collection.collection_date <= end_date
		).group_by(Collection.farmer_id).all()
	print(trips)

	data = []
	for trip in trips:
		farmer = get_farmer(trip[0])
		farmer_data = {}
		farmer_data['farmer_id'] = trip[0]
		farmer_data['supplier_no'] = farmer.supplier_no
		farmer_data['farmer_name'] = farmer.fullname
		farmer_data['cumm_weight'] = trip[1]

		data.append(farmer_data)

	return render_template('reports/farmer_cumm.html', data=data, start_date=start_date, end_date=end_date)

@reports.route('/cumm-route', methods=['GET', 'POST'])
@login_required
def cumm_route():
	form = CollectionPerGrader()

	start_date = datetime.strptime(form.start_date.data, "%m/%d/%Y %H:%M %p").date() 
	end_date = datetime.strptime(form.end_date.data, "%m/%d/%Y %H:%M %p").date() 

	trips = db.session.query(Collection.route_id, func.sum(Collection.produce_weight)
		).filter(Collection.collection_date  >= start_date, Collection.collection_date <= end_date
		).group_by(Collection.farmer_id).all()
	print(trips)

	data = []
	for trip in trips:
		farmer = get_farmer(trip[0])
		farmer_data = {}
		farmer_data['farmer_id'] = trip[0]
		farmer_data['supplier_no'] = farmer.supplier_no
		farmer_data['farmer_name'] = farmer.fullname
		farmer_data['cumm_weight'] = trip[1]

		data.append(farmer_data)

	return render_template('reports/farmer_cumm.html', data=data, start_date=start_date, end_date=end_date)
