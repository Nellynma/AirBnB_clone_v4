#!/usr/bin/python3
"""New view for City objects that handles all default RestFul API actions
"""
import os
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """Retrieves all city objects of a state"""
    state = storage.get(State, state_id)
    if request.method == 'GET':
        if not state:
            abort(404)
        if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
            all_cities = state.cities
        else:
            all_cities = state.cities()
        return jsonify([value.to_dict() for value in all_cities])

    elif request.method == "POST":
        if not state:
            abort(404)
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, "Not a JSON")
        if 'name' in body_request:
            body_request.update({"state_id": state_id})
            new_city = City(**body_request)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
        else:
            abort(400, "Missing name")


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """Retrieves, updates and deletes city objects by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            new_values = request.get_json()
        else:
            abort(400, "Not a JSON")
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in new_values.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
