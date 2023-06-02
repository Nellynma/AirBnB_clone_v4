#!/usr/bin/python3
"""Amenities view"""
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """Retrieves all the amenities objects"""
    if request.method == 'GET':
        all_amenities = storage.all(Amenity)
        amenities = []
        for key, value in all_amenities.items():
            amenities.append(value.to_dict())
        return jsonify(amenities)

    elif request.method == 'POST':
        # convert JSON request to dict
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # instantiate, store, and return new Amenity object
        if 'name' in body_request:
            new_amenity = Amenity(**body_request)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        else:  # if request does not contain required attribute
            abort(400, 'Missing name')


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    """Retrieves, deletes or updates  an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            new_values = request.get_json()
        else:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in new_values.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
