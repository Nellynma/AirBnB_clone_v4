#!/usr/bin/python3
"""Entry point of the api"""
from flask import Flask
from flask_cors import CORS
from flask import make_response
from flask import jsonify
from models import storage
from api.v1.views import app_views
import os
#from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')

storage.reload()

@app.teardown_appcontext
def close_storage(exception=None):
    """Calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles 404 erros"""
    return make_response(jsonify({'error': 'Not found'}), 404)

"""
@app.errorhandler(400)
def bad_request(error):
    return error.description
    #if error.description == 'Not a JSON':
        #return make_response(jsonify({'error': 'Not a JSON'}), 400)
"""

if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True, debug=True)
