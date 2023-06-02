#!/usr/bin/python3
"""view for users"""
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from models import storage
from models.user import User
from api.v1.views import app_views

@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """Retrieves all the user objects"""
    if request.method == 'GET':
        all_users = storage.all(User)
        users = []
        for key, value in all_users.items():
            users.append(value.to_dict())
        return jsonify(users)

    elif request.method == 'POST':
        # convert JSON request to dict
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # check for missing attributes
        if 'email' not in body_request:
            abort(400, 'Missing email')
        elif 'password' not in body_request:
            abort(400, 'Missing password')
        # instantiate, store, and return new User object
        else:
            new_user = User(**body_request)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    """Retrieves, deletes or updates  a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            new_values = request.get_json()
        else:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in new_values.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
