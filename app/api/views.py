from flask import jsonify, request
from ..models import Factory, CollectionCentre, Produce, Farmer, Customer, User, Collection, Season, Trip, Vehicle, AppUser, Driver, Route
from . import api
from app import db

@api.route('/factories/',  methods=['GET'])
def get_factories():
	return jsonify({'factories':[ s.to_json() for s in Factory.query.all() ]})

@api.route('/centres/',  methods=['GET'])
def get_centres():
	return jsonify({'centres':[ s.to_json() for s in CollectionCentre.query.all() ]})

@api.route('/produce/',  methods=['GET'])
def get_produce():
	return jsonify({'produce':[ s.to_json() for s in Produce.query.all() ]})


@api.route('/farmers/',  methods=['GET'])
def get_farmers():
	return jsonify({'farmers':[ s.to_json() for s in Farmer.query.all() ]})

@api.route('/users/',  methods=['GET'])
def get_users():
	return jsonify({'users':[ s.to_json() for s in AppUser.query.all() ]})

@api.route('/seasons/',  methods=['GET'])
def get_seasons():
	return jsonify({'seasons':[ s.to_json() for s in Season.query.all() ]})


@api.route('/trips/',  methods=['GET'])
def get_trips():
	return jsonify({'trips':[ s.to_json() for s in Trip.query.filter_by(status="OPEN") ]})



@api.route('/vehicles/',  methods=['GET'])
def get_vehicles():
	return jsonify({'vehicles':[ s.to_json() for s in Vehicle.query.all() ]})



@api.route('/graders/',  methods=['GET'])
def get_graders():
	return jsonify({'graders':[ s.to_json() for s in AppUser.query.filter_by(role_id=2) ]})


@api.route('/drivers/',  methods=['GET'])
def get_drivers():
	return jsonify({'drivers':[ s.to_json() for s in Driver.query.all() ]})




@api.route('/routes/',  methods=['GET'])
def get_routes():
	return jsonify({'routes':[ s.to_json() for s in Route.query.all() ]})

def update_total_recieved(produce_weight, trip_id):
	print(produce_weight, trip_id)
	trip = Trip.query.filter_by(id=trip_id).first()
	trip.total_weight_collected = (trip.total_weight_collected) + float(produce_weight)
	db.session.add(trip)
	db.session.commit()


@api.route('/collections/new', methods=['POST'])
def new_collection():
	c = Collection().from_json(request.json)
	try:
		update_total_recieved(c.produce_weight, c.trip_id)
		c.id
		db.session.add(c)
		db.session.commit()
		response = jsonify({"record_id":c.id})
		response.status_code = 201

	except AttributeError:
		print(c)
		response = jsonify({"error_message":c})
		response.status_code = 400
	return response 