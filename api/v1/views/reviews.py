#!/usr/bin/python3
"""views for reviews"""
import os
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews(place_id):
    """Retrieves all review objects of a place"""
    if request.method == 'GET':
        place  = storage.get(Place, place_id)
        if not place:
            abort(404)
        all_reviews = place.reviews
        reviews = []
        for review in all_reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)

    elif request.method == "POST":
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, "Not a JSON")
        if 'user_id' not in body_request:
            abort(400, "Missing user_id")
        elif 'text' not in body_request:
            abort(400, "Missing text")
        else:
            users = storage.all(User)
            user_id = body_request['user_id']
            all_user_ids = [user_ids.id for user_ids in users.values()]
            if user_id not in all_user_ids:
                abort(404)
            place_key = "Place." + place_id
            if place_key not in places:
                abort(404)
            body_request.update({"place_id": place_id})
            new_review = Review(**body_request)
            storage.new(new_review)
            storage.save()
            return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review(review_id):
    """Retrieves, deletes and updates review objects by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            new_values = request.get_json()
        else:
            abort(400, "Not a JSON")
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in new_values.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
