import io

from flask import Flask, request, jsonify, make_response, flash
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import swiftclient.service
from swiftclient.service import SwiftService
import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.after_request
def append_cors_origin(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.before_request
def append_cors_origin(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@cross_origin()#supports_credentials=True)
@app.route('/upload_file')
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