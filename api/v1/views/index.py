#!/usr/bin/python3
"""view for API status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.place import Place


objects = {'cities': City,
           'users': User,
           'amenities': Amenity,
           'reviews': Review,
           'states': State,
           'places': Place}


@app_views.route('/status')
def status():
    """Returns the status of our api"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    stats = {}
    for key, value in objects.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
