#!/usr/bin/python3
"""views for places"""
import os
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.state import State
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def places(city_id):
    """Retrieves all place objects of a city"""
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if not city:
            abort(404)
        all_places = city.places
        places = []
        for place in all_places:
            places.append(place.to_dict())
        return jsonify(places)
    elif request.method == 'POST':
        if not city:
            abort(404)
        if request.is_json:
            values = request.get_json()
        else:
            abort(400, 'Not a JSON')

        if 'name' not in values:
            abort(400, 'Missing name')
        elif 'user_id' not in values:
            abort(400, 'Missing user_id')

        users = storage.all(User)
        if ('User.' + body_request['user_id']) not in users.keys():
            abort(404)

        values.update({'city_id': city_id})
        new_place = Place(**values)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place(place_id):
    """Retrieves, updates and deletes places by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            new_values = request.get_json()
        else:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in new_values.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
        create new place obj through city association using POST
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    else:
        obj_data = request.get_json()
        city = storage.get("City", city_id)
        user = storage.get("User", obj_data['user_id'])
        if city is None or user is None:
            abort(404)
        obj_data['city_id'] = city.id
        obj_data['user_id'] = user.id
        obj = Place(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
        update existing place object using PUT
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ("id", "user_id", "created_at", "updated_at")
    for k, v in obj_data.items():
        if k not in ignore:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
