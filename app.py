import io

from flask import Flask, request, jsonify, make_response, flash
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import swiftclient.service
from swiftclient.service import SwiftService
import datetime

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

# cors = CORS(app, resources={r"/upload_file": {"origins": "http://localhost:5000"}})
#
#
# def build_preflight_response():
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response
#
#
# def build_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#
#     return response
#

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# @app.before_request
# def append_cors_origin(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response

def crossdomain(origin=None, methods=None, headers=None,
       max_age=21600, attach_to_all=True,
       automatic_options=True):
    if methods is not None:
     methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
     headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
     origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
     max_age = max_age.total_seconds()

    def get_methods():
     if methods is not None:
      return methods

     options_resp = current_app.make_default_options_response()
     return options_resp.headers['allow']

    def decorator(f):
     def wrapped_function(*args, **kwargs):
      if automatic_options and request.method == 'OPTIONS':
       resp = current_app.make_default_options_response()
      else:
       resp = make_response(f(*args, **kwargs))
      if not attach_to_all and request.method != 'OPTIONS':
       return resp

      h = resp.headers

      h['Access-Control-Allow-Origin'] = origin
      h['Access-Control-Allow-Methods'] = get_methods()
      h['Access-Control-Max-Age'] = str(max_age)
      if headers is not None:
       h['Access-Control-Allow-Headers'] = headers
      return resp

     f.provide_automatic_options = False
     return update_wrapper(wrapped_function, f)
    return decorator

# @crossdomain(origin="*")
@app.route('/upload_file', methods=['POST'])
@cross_origin( supports_credentials=True,
               headers=['DNT','User-Agent','X-Requested-With',
                        'If-Modified-Since','Cache-Control',
                        'Content-Type','Range'], origin="*")
def upload_file():
    user = 'test:tester'
    key = 'testing'
    authurl = globals()["SWIFT_URI"] + ":8080/auth/v1.0"
    container_name = "test_ui-react"
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(message="No file to upload")
    file = request.files["file"]
    if file.filename == '':
        flash('No selected file')
        return "No file"
    filename = secure_filename(file.filename)

    file.save(filename)

    return jsonify(message="Ok")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')