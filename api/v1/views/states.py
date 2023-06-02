#!/usr/bin/python3
"""View to handle API actions related to State objects
"""
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """Retrieves all the state objects"""
    if request.method == 'GET':
        all_states = storage.all(State)
        return jsonify([value.to_dict() for value in all_states.values()])

    elif request.method == 'POST':
        # convert JSON request to dict
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # instantiate, store, and return new State object
        if 'name' in body_request:
            new_state = State(**body_request)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:  # if request does not contain required attribute
            abort(400, 'Missing name')


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    """Retrieves, deletes or updates  a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
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
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
